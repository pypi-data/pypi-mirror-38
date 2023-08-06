import logging
from functools import wraps
from typing import List, Optional, SupportsInt  # noqa

import aiomysql
import pymysql
from pypika import MySQLQuery

from tortoise.backends.base.client import (BaseDBAsyncClient, BaseTransactionWrapper,
                                           ConnectionWrapper, SingleConnectionWrapper)
from tortoise.backends.mysql.executor import MySQLExecutor
from tortoise.backends.mysql.schema_generator import MySQLSchemaGenerator
from tortoise.exceptions import (ConfigurationError, DBConnectionError, IntegrityError,
                                 OperationalError, TransactionManagementError)
from tortoise.transactions import current_transaction_map


def translate_exceptions(func):
    @wraps(func)
    async def wrapped(self, query, *args):
        try:
            return await func(self, query, *args)
        except (pymysql.err.OperationalError, pymysql.err.ProgrammingError,
                pymysql.err.DataError, pymysql.err.InternalError,
                pymysql.err.NotSupportedError) as exc:
            raise OperationalError(exc)
        except pymysql.err.IntegrityError as exc:
            raise IntegrityError(exc)
    return wrapped


class MySQLClient(BaseDBAsyncClient):
    query_class = MySQLQuery
    executor_class = MySQLExecutor
    schema_generator = MySQLSchemaGenerator

    def __init__(self, user: str, password: str, database: str, host: str, port: SupportsInt,
                 **kwargs) -> None:
        super().__init__(**kwargs)

        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = int(port)  # make sure port is int type

        self.template = {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
        }

        self._db_pool = None  # Type: Optional[aiomysql.Pool]
        self._connection = None  # Type: Optional[aiomysql.Connection]

        self._transaction_class = type(
            'TransactionWrapper', (TransactionWrapper, self.__class__), {}
        )

    async def create_connection(self) -> None:
        try:
            if not self.single_connection:
                self._db_pool = await aiomysql.create_pool(db=self.database, **self.template)
            else:
                self._connection = await aiomysql.connect(db=self.database, **self.template)
            self.log.debug(
                'Created connection with params: user=%s database=%s host=%s port=%s',
                self.user, self.database, self.host, self.port
            )
        except pymysql.err.OperationalError:
            raise DBConnectionError(
                "Can't connect to MySQL server: "
                'user={user} database={database} host={host} port={port}'.format(
                    user=self.user, database=self.database, host=self.host, port=self.port
                )
            )

    async def close(self) -> None:
        if self._db_pool:
            self._db_pool.close()
        if self._connection:
            self._connection.close()

    async def db_create(self) -> None:
        single_connection = self.single_connection
        self.single_connection = True
        self._connection = await aiomysql.connect(
            **self.template
        )
        await self.execute_script(
            'CREATE DATABASE {}'.format(self.database)
        )
        self._connection.close()  # type: ignore
        self.single_connection = single_connection

    async def db_delete(self) -> None:
        single_connection = self.single_connection
        self.single_connection = True
        self._connection = await aiomysql.connect(
            **self.template
        )
        try:
            await self.execute_script('DROP DATABASE {}'.format(self.database))
        except pymysql.err.DatabaseError:
            pass
        self._connection.close()  # type: ignore
        self.single_connection = single_connection

    def acquire_connection(self):
        if not self.single_connection:
            return self._db_pool.acquire()
        else:
            return ConnectionWrapper(self._connection)

    def _in_transaction(self):
        if self.single_connection:
            return self._transaction_class(self.connection_name, connection=self._connection)
        else:
            return self._transaction_class(self.connection_name, pool=self._db_pool)

    @translate_exceptions
    async def execute_insert(self, query: str, values: list) -> int:
        self.log.debug('%s: %s', query, values)
        async with self.acquire_connection() as connection:
            async with connection.cursor() as cursor:
                # TODO: Use prepared statement, and cache it
                await cursor.execute(query, values)
                return cursor.lastrowid  # return auto-generated id

    @translate_exceptions
    async def execute_query(self, query: str) -> List[aiomysql.DictCursor]:
        self.log.debug(query)
        async with self.acquire_connection() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                return await cursor.fetchall()

    @translate_exceptions
    async def execute_script(self, query: str) -> None:
        self.log.debug(query)
        async with self.acquire_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query)

    async def get_single_connection(self):
        if self.single_connection:
            return self._single_connection_class(self.connection_name, self._connection, self)
        else:
            connection = await self._db_pool._acquire()
            return self._single_connection_class(self.connection_name, connection, self)

    async def release_single_connection(self, single_connection):
        if not self.single_connection:
            await self._db_pool.release(single_connection.connection)


class TransactionWrapper(MySQLClient, BaseTransactionWrapper):
    def __init__(self, connection_name, pool=None, connection=None):
        if pool and connection:
            raise ConfigurationError('You must pass either connection or pool')
        self.connection_name = connection_name
        self._connection = connection
        self.log = logging.getLogger('db_client')
        self._pool = pool
        self.single_connection = True
        self._single_connection_class = type(
            'SingleConnectionWrapper', (SingleConnectionWrapper, self.__class__), {}
        )
        self._transaction_class = self.__class__
        self._finalized = False
        self._old_context_value = None

    def acquire_connection(self):
        return ConnectionWrapper(self._connection)

    async def _get_connection(self):
        return await self._pool._acquire()

    async def start(self):
        if not self._connection:
            self._connection = await self._get_connection()
        await self._connection.begin()
        current_transaction = current_transaction_map[self.connection_name]
        self._old_context_value = current_transaction.get()
        current_transaction.set(self)

    async def commit(self):
        if self._finalized:
            raise TransactionManagementError('Transaction already finalised')
        self._finalized = True
        await self._connection.commit()
        if self._pool:
            await self._pool.release(self._connection)
            self._connection = None
        current_transaction_map[self.connection_name].set(self._old_context_value)

    async def rollback(self):
        if self._finalized:
            raise TransactionManagementError('Transaction already finalised')
        self._finalized = True
        await self._connection.rollback()
        if self._pool:
            await self._pool.release(self._connection)
            self._connection = None
        current_transaction_map[self.connection_name].set(self._old_context_value)
