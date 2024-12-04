from typing import TYPE_CHECKING

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
    from typing import Any
    from sqlalchemy import ColumnElement


class AsyncDatabase:
    def __init__(
        self,
        user: "str",
        password: "str",
        dialect: "str" = "asyncpg",
        host: "str" = "localhost",
        port: "int" = 5432,
        database_name: "str" = "postgres",
    ):
        url = self.get_url(dialect, user, password, host, port, database_name)
        engine = self.create_engine(url)
        session_factory = self.create_session_type(engine)
        self.query_executor = self.set_query_executor(session_factory)

    def get_url(
        self,
        dialect: "str",
        user: "str",
        password: "str",
        host: "str",
        port: "int",
        database_name: "str",
    ):
        return f"postgresql+{dialect}://{user}:{password}@{host}:{port}/{database_name}"

    def create_engine(self, url: "str"):
        return create_async_engine(url)

    def create_session_type(self, engine: "AsyncEngine"):
        return async_sessionmaker(engine)

    def set_query_executor(self, session_factory: "async_sessionmaker[AsyncSession]"):
        return AsyncQueryExecutor(session_factory)

    async def select[
        T
    ](self, entity: "type[T]", where_clause: "ColumnElement[bool] | None" = None):
        return await self.query_executor.select(entity, where_clause)

    async def insert[T](self, entity: "type[T]", values_params: "list[dict[str, Any]]"):
        return await self.query_executor.insert(entity, values_params)

    async def update[
        T
    ](
        self,
        entity: "type[T]",
        where_clause: "ColumnElement[bool]",
        value_params: "dict[str, Any]",
    ):
        return await self.query_executor.update(entity, where_clause, value_params)

    async def update_by_primary_key[
        T
    ](self, entity: "type[T]", values_params: "list[dict[str, Any]]"):
        return await self.query_executor.update_by_primary_key(entity, values_params)

    async def delete[T](self, entity: "type[T]", where_clause: "ColumnElement[bool]"):
        return await self.query_executor.delete(entity, where_clause)


class AsyncQueryExecutor:
    def __init__(self, session_factory: "async_sessionmaker[AsyncSession]"):
        self.session_factory = session_factory

    def session(self):
        return self.session_factory()

    async def select[
        T
    ](self, entity: "type[T]", where_clause: "ColumnElement[bool] | None" = None):
        async with self.session() as session:
            stmt = select(entity)
            if where_clause is not None:
                stmt = stmt.where(where_clause)
            result = await session.scalars(stmt)

            return result.all()

    async def insert[T](self, entity: "type[T]", values_params: "list[dict[str, Any]]"):
        async with self.session() as session:
            stmt = insert(entity).values().returning(entity)
            result = await session.scalars(stmt, values_params)

            return result.all()

    async def update[
        T
    ](
        self,
        entity: "type[T]",
        where_clause: "ColumnElement[bool]",
        value_params: "dict[str, Any]",
    ):
        async with self.session() as session:
            stmt = (
                update(entity)
                .where(where_clause)
                .values(**value_params)
                .returning(entity)
            )
            result = await session.scalars(stmt)

            return result.all()

    async def update_by_primary_key[
        T
    ](self, entity: "type[T]", values_params: "list[dict[str, Any]]"):
        async with self.session() as session:
            stmt = update(entity)
            result = await session.scalars(stmt, values_params)

            return result.all()

    async def delete[T](self, entity: "type[T]", where_clause: "ColumnElement[bool]"):
        async with self.session() as session:
            stmt = delete(entity).where(where_clause).returning(entity)
            result = await session.scalars(stmt)

            return result.all()
