import logging

from ..exception import DatabaseError
from ..exception import ExceptionWrapper
from ..exception import IntegrityError
from ..exception import OperationalError
from ..field import BaseField
from ..table import BaseTable

EXCEPTIONS = {
    'ConstraintError': IntegrityError,
    'DatabaseError': DatabaseError,
    'IntegrityError': IntegrityError,
    'OperationalError': OperationalError,
    'Exception': Exception}

__exception_wrapper__ = ExceptionWrapper(EXCEPTIONS)


class Query:
    __create_table_template__ = 'CREATE TABLE {table_name} (\n{columns_definition}\n{foreign_keys_definition}\n)'
    __drop_table_template__ = 'DROP TABLE {table_name}'
    __insert_template__ = 'INSERT INTO {table_name}({columns_names})\nVALUES ({values})'
    __select_template__ = 'SELECT {columns_names} FROM {table_name}'
    __update_template__ = 'UPDATE {table_name} SET\n{columns_values}'
    __delete_template__ = 'DELETE FROM {table_name}'

    def __init__(self, *args, query_str=None, connect=None):
        super().__init__()

        self.__connect = connect
        if query_str is None:
            query_str = ''
        self.__query_str = query_str
        self.__join_str = ''
        self.__filter_str = ''

        self.__query_list = []

        self.__tables = set()
        self.__fields = []
        self.__main_table = None

        with __exception_wrapper__:
            for arg in args:
                if isinstance(arg, BaseField):
                    self.__fields.append(arg)
                elif issubclass(arg, BaseTable):
                    self.__tables.add(arg)
                    self.__fields.extend([field[1] for field in arg.get_fields()])
                else:
                    raise Exception(
                        "'{}' must be instance or subclass of '{}'".format(arg.__name__, BaseField.__name__))

        if self.__fields:
            self.__main_table = self.__fields[0].table_class

    def __add_to_query_list__(self, query_str):
        self.__query_list.append(query_str)

    @property
    def query_str(self):
        query = self.__query_str
        if self.__join_str:
            query += self.__join_str
        if self.__filter_str:
            query += '\nWHERE {}'.format(self.__filter_str)
        return query

    @classmethod
    def get_fields(cls):
        """
        возвращает набор полей таблицы
        :return: список пар [(название колонки, инстанс колонки),..]
        """
        return [(attr, getattr(cls, attr)) for attr in cls.__dict__ if isinstance(getattr(cls, attr), BaseField)]

    @property
    def query_list(self):
        query_list = self.__query_list[:]
        if not query_list:
            query_list.append(self.query_str)

        return query_list

    def __get_drop_table_script__(self, cls):
        return self.__drop_table_template__.format(table_name=cls.__table_name__)

    def __get_create_table_script__(self, cls):
        fields = cls.get_fields()
        columns_definition = ',\n'.join(('{} {}'.format(field[0], field[1].definition) for field in fields))
        foreign_keys_definition = '\n'.join(
            ', {}'.format(field[1].foreign_key_definition) for field in fields if field[1].foreign_key_definition)

        return self.__create_table_template__.format(
            table_name=cls.__table_name__,
            columns_definition=columns_definition,
            foreign_keys_definition=foreign_keys_definition)

    def __get_insert_script__(self, table_name, column_value_map):
        return self.__insert_template__.format(
            table_name=table_name,
            columns_names=', '.join(column_value_map.keys()),
            values=', '.join(map(str, column_value_map.values()))
        )

    def get_update_script(self, table_name, columns_values):
        return self.__update_template__.format(
            table_name=table_name,
            columns_values=',\n'.join(['{} = {}'.format(column, value) for column, value in columns_values.items()])
        )

    def __get_select_script__(self, table_name, columns_names):
        return self.__select_template__.format(columns_names=', '.join(columns_names), table_name=table_name)

    def __set_query_str__(self, query):
        self.__query_str = query

    def add_join_str(self, join_str):
        self.__join_str += join_str

    def set_query_str(self, query):
        self.__query_str = query

    def add_filter_str(self, filter_str, logical_operator):
        self.__filter_str += (' {} '.format(logical_operator) if self.__filter_str else '').join(filter_str)

    def get_delete_script(self, table_name):
        return self.__delete_template__.format(table_name=table_name)

    def create(self):
        """
        Создать Query со скриптами создания таблиц
        :return: инстанс Query
        """
        for table in self.__tables:
            self.__add_to_query_list__(self.__get_create_table_script__(table))
        return self

    def insert(self, *table_records):
        """
        Создать Query со скриптом insert
        :param table_records: инстансы классов-таблиц
        :return: инстанс Query
        """
        for table_record in table_records:
            self.__add_to_query_list__(self.__get_insert_script__(
                table_name=table_record.__class__.__table_name__,
                column_value_map=table_record.column_value_map
            ))
        return self

    def select(self):
        """
        Создать Query со скриптом select
        :return: инстанс Query
        """

        columns_names = [col.full_name for col in self.__fields]

        self.__set_query_str__(self.__get_select_script__(self.__main_table.__table_name__, columns_names))
        return self

    def filter(self, *condition_expressions, logical_operator_inner=None, logical_operator_outer=None):
        """
        Добавляет условие ограничения
        :param condition_expressions: условие ограничения (Table.column == 10, Table.column == Table2.column2)
        :param logical_operator_inner: логический оператор для внутреннего соединения переданных условий
        :param logical_operator_outer: логический оператор для внешнего соединения переданных условий
        :return: инстанс Query
        """
        if logical_operator_inner is None:
            logical_operator_inner = 'AND'
        if logical_operator_outer is None:
            logical_operator_outer = 'AND'

        assert logical_operator_inner.upper() in ('AND', 'OR'), 'logical_operator_inner choice of OR, AND'
        assert logical_operator_outer.upper() in ('AND', 'OR'), 'logical_operator_outer choice of OR, AND'

        filter_condition = '({})'.format((' {} '.format(logical_operator_inner).join(condition_expressions)))
        logging.debug(
            "Getting filter condition: {} and logical operator: {}".format(filter_condition, logical_operator_outer))
        self.add_filter_str(filter_condition, logical_operator_outer)

        return self

    def drop(self):
        """
        Создать Query со скриптами удаления таблиц
        :return: инстанс Query
        """
        for table in self.__tables:
            self.__add_to_query_list__(self.__get_drop_table_script__(table))
        return self

    def update(self, **kwargs):
        """
        Создать Query со скриптом update
        :param kwargs: поля таблицы для обновления
        :return: инстанс Query
        """

        columns_values = {
            field_name: self.__main_table.get_field_by_name(field_name).__class__.quoted_value(value)
            for field_name, value in kwargs.items()
        }

        self.set_query_str(self.get_update_script(
            table_name=self.__main_table.__table_name__,
            columns_values=columns_values
        ))
        return self

    def delete(self):
        """
        Создать Query со скриптом delete
        :return: инстанс Query
        """
        self.set_query_str(self.get_delete_script(table_name=self.__main_table.__table_name__))
        return self

    def join(self, table, auto_join=True):
        """
        Добавляет join таблицы к запросу
        :param table: класс-таблица
        :param auto_join: флаг(генерировать условие присеодинения для таблиц с FK, если True)
        :return: инстанс Query
        """
        join_str = '\nJOIN {}'.format(table.__table_name__)
        if auto_join:
            field_foreign_key = self.__main_table.get_foreign_field_by_table(table) or \
                                table.get_foreign_field_by_table(self.__main_table)
            if field_foreign_key:
                join_str += ' ON {} = {}'.format(field_foreign_key.full_name, field_foreign_key.foreign_key.full_name)

        self.add_join_str(join_str)
        logging.debug("Getting join string: {}".format(join_str))
        return self

    def execute(self):
        """
        Выполняет запросы, собранные в инстансе Query
        :return: курсор
        """

        with __exception_wrapper__:
            cur = self.__connect.cursor()
            try:
                for query in self.query_list:
                    logging.debug("Execute query: {}".format(query))
                    cur.execute(query)
            except Exception as e:
                self.__connect.rollback()
                raise e
            else:
                self.__connect.commit()
        return cur
