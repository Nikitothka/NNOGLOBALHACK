import asyncpg
from typing import Any, Dict, List, Optional, Union


class Database:
    def __init__(self, dsn: str):
        """
        Инициализация класса Database с подключением к базе данных PostgreSQL.

        :param dsn: Строка подключения к базе данных.
        """
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Создание пула подключений к базе данных."""
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def disconnect(self):
        """Закрытие пула подключений."""
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args: Any) -> None:
        """
        Выполнение запроса без возвращения результата.

        :param query: SQL-запрос.
        :param args: Аргументы для SQL-запроса.
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, *args)

    async def fetch(self, query: str, *args: Any) -> List[asyncpg.Record]:
        """
        Выполнение запроса с возвращением результатов.

        :param query: SQL-запрос.
        :param args: Аргументы для SQL-запроса.
        :return: Список записей (асинхронный).
        """
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args: Any) -> Optional[asyncpg.Record]:
        """
        Выполнение запроса с возвращением одной записи.

        :param query: SQL-запрос.
        :param args: Аргументы для SQL-запроса.
        :return: Одна запись или None.
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def create(self, table: str, data: Dict[str, Any]) -> None:
        """
        Создание новой записи в указанной таблице.

        :param table: Название таблицы.
        :param data: Словарь с данными для вставки.
        """
        keys = ', '.join(data.keys())
        values = ', '.join(f'${i + 1}' for i in range(len(data)))
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        await self.execute(query, *data.values())

    async def read(self, table: str, conditions: Optional[Dict[str, Any]] = None) -> List[asyncpg.Record]:
        """
        Чтение записей из указанной таблицы с возможными условиями.

        :param table: Название таблицы.
        :param conditions: Словарь с условиями для WHERE.
        :return: Список записей.
        """
        query = f'SELECT * FROM {table}'
        if conditions:
            where_clause = ' AND '.join(f'{k} = ${i + 1}' for i, k in enumerate(conditions.keys()))
            query += f' WHERE {where_clause}'
            return await self.fetch(query, *conditions.values())
        return await self.fetch(query)

    async def update(self, table: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> None:
        """
        Обновление записей в указанной таблице.

        :param table: Название таблицы.
        :param data: Словарь с данными для обновления.
        :param conditions: Словарь с условиями для WHERE.
        """
        set_clause = ', '.join(f'{k} = ${i + 1}' for i, k in enumerate(data.keys()))
        where_clause = ' AND '.join(f'{k} = ${i + len(data) + 1}' for i, k in enumerate(conditions.keys()))
        query = f'UPDATE {table} SET {set_clause} WHERE {where_clause}'
        await self.execute(query, *data.values(), *conditions.values())

    async def delete(self, table: str, conditions: Dict[str, Any]) -> None:
        """
        Удаление записей из указанной таблицы.

        :param table: Название таблицы.
        :param conditions: Словарь с условиями для WHERE.
        """
        where_clause = ' AND '.join(f'{k} = ${i + 1}' for i, k in enumerate(conditions.keys()))
        query = f'DELETE FROM {table} WHERE {where_clause}'
        await self.execute(query, *conditions.values())
