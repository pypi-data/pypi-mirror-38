import sqlite3

from .query import Query


class Database:

    def __init__(self, db):
        self.__connect = sqlite3.connect(db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.__connect.close()

    def query(self, *args, query_str=None):
        """
        Получить инстанс класса запроса
        :param args: инстансы класса-поля, класс-таблицы
        :param query_str: raw sql
        :return: инстанс класса запроса
        """
        return Query(*args, query_str=query_str, connect=self.__connect)
