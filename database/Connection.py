import sqlite3
import aiosqlite
from asyncio import get_event_loop
from config.Config import Config
from database.backup_tools import backup
from database.database_log.log import log
import os


class Connection:
    """Class connection - центр управления базой данных"""

    def __init__(self):
        loop = get_event_loop()
        self.connection: aiosqlite.Connection = loop.run_until_complete(
            aiosqlite.connect(os.path.join(os.path.dirname(__file__), Config.db_name)))
        self.__transactions: int = 0

        log.info(f'successful connect to {Config.db_name}')

    async def __on_request(self, sql_request: str):
        """Coro handler on_request(sql_request: str)
            Works after request to database
        """

        if "select" in sql_request.lower():
            return

        self.__transactions += 1
        if self.__transactions == Config.transactions_to_backup:
            self.__transactions = 0
            await backup()

    async def request(self, sql_request: str, values=()) -> sqlite3.Cursor:
        """coro request(sql_request, values)

            :arg sql_request - Your sql request
            :arg values - Value for substitution

            :return sqlite3.Cursor

            Ex:
                values = await (await request("SELECT user_id FROM users WHERE balance = ?"), (100, )).fetchall()
        """

        cursor = await self.connection.cursor()
        statement = await cursor.execute(sql_request, values)

        await self.connection.commit()
        await self.__on_request(sql_request)

        log.debug(
            f'request to {Config.db_name}. sql_request: {sql_request}, values: {values}, transaction: {self.__transactions}')

        return statement


connect: Connection = Connection()
