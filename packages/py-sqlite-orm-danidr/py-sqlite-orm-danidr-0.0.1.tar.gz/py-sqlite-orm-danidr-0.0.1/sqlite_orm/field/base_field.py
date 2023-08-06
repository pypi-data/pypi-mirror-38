class BaseField:
    __type_name__ = None
    __template_definition__ = '{TYPE} {NOT_NULL} {PRIMARY_KEY} {DEFAULT_VALUE} {AUTOINCREMENT}'
    __template_foreign_key_definition__ = 'FOREIGN KEY ({self_name}) REFERENCES {table_name}({field_name})'
    __template_cmp__ = '{field_name} {operator} {other}'

    def __init__(self, not_null=False, primary_key=False, foreign_key=None, default_value=None):
        """

        :param not_null: является ли поле not null
        :param primary_key: является ли поле первичным ключом
        :param foreign_key: ссылка на внешний ключ
        :param default_value: значение по умолчанию
        """

        self.primary_key = primary_key
        self.not_null = self.primary_key or not_null
        self.foreign_key = foreign_key
        self.default_value = self.__class__.value(default_value)
        self.table_class = None
        self.auto_increment = None

    @property
    def type_name(self):
        return self.__type_name__

    @property
    def definition(self):
        return self.__template_definition__.format(**self.__definition_dict__)

    @property
    def __definition_dict__(self):
        return {
            'TYPE': self.type_name,
            'NOT_NULL': 'NOT NULL' if self.not_null else '',
            'PRIMARY_KEY': 'PRIMARY KEY' if self.primary_key else '',
            'DEFAULT_VALUE': 'DEFAULT %s' % self.default_value if self.default_value is not None else '',
            'AUTOINCREMENT': 'AUTOINCREMENT' if self.auto_increment is not None else '',
        }

    @property
    def foreign_key_definition(self):
        return self.foreign_key is not None and self.__template_foreign_key_definition__.format(
            self_name=self.name,
            table_name=self.foreign_key.table_name,
            field_name=self.foreign_key.name
        )

    @property
    def table_name(self):
        return self.table_class.__table_name__

    @property
    def name(self):
        return self.table_class.get_field_name(self)

    @staticmethod
    def value(val):
        return val

    def set_table_class(self, cls):
        self.table_class = cls

    @property
    def full_name(self):
        return '{}.{}'.format(self.table_name, self.name)

    @classmethod
    def quoted_value(cls, val):
        return 'NULL' if val is None else cls.value(val)

    def __repr__(self):
        return self.full_name

    def __fill_template_cmp(self, field_name, operator, other):
        return self.__template_cmp__.format(field_name=field_name, operator=operator, other=repr(other))

    def __eq__(self, other):
        return self.__fill_template_cmp(self, '=', other)

    def __ne__(self, other):
        return self.__fill_template_cmp(self, '!=', other)

    def __lt__(self, other):
        return self.__fill_template_cmp(self, '<', other)

    def __gt__(self, other):
        return self.__fill_template_cmp(self, '>', other)

    def __le__(self, other):
        return self.__fill_template_cmp(self, '<=', other)

    def __ge__(self, other):
        return self.__fill_template_cmp(self, '>=', other)
