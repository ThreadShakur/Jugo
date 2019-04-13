import json

class DataType():
    max_length = None
    default = None
    extra = ''
    unsigned = False

    # Handilng data before sql request
    def pre_handling(self, value):
        return value

    # Handling data after sql request
    def post_handling(self, value):
        return value


class Index():
    def __init__(self, *fields):
        self.fields = fields


class BigInteger(DataType):
    definition = 'BIGINT'

    def __init__(self, unsigned=False, default=None):
        self.unsigned = unsigned
        self.default = default

    definition_f = lambda self: 'BIGINT'
    default_f = lambda self: f'DEFAULT {self.default}' if self.default is not None else ''
    extra_f = lambda self: self.extra + ' UNSIGNED' if self.unsigned else ''


class Integer(DataType):
    definition = 'INT'

    def __init__(self, default=None, unsigned=False, auto_increment=False):
        self.default = default
        self.unsigned = unsigned
        self.auto_increment = auto_increment
        if auto_increment:
            self.extra = 'AUTO_INCREMENT'
        

    definition_f = lambda self: 'INT'
    default_f = lambda self: f'DEFAULT {self.default}' if self.default is not None else ''
    extra_f = lambda self: self.extra + ' PRIMARY KEY' if self.auto_increment else '' + ' UNSIGNED' if self.unsigned else ''


class MediumInteger(DataType):
    definition = 'MEDIUMINT'

    def __init__(self, unsigned=False, default=None):
        self.unsigned = unsigned
        self.default = default

    definition_f = lambda self: 'MEDIUMINT'
    default_f = lambda self: f'DEFAULT {self.default}' if self.default is not None else ''
    extra_f = lambda self: self.extra + ' UNSIGNED' if self.unsigned else ''


class SmallInteger(DataType):
    definition = 'SMALLINT'

    def __init__(self, unsigned=False, default=None):
        self.unsigned = unsigned
        self.default = default

    definition_f = lambda self: 'SMALLINT'
    default_f = lambda self: f'DEFAULT {self.default}' if self.default is not None else ''
    extra_f = lambda self: self.extra + ' UNSIGNED' if self.unsigned else ''


class TinyInteger(DataType):
    definition = 'TINYINT'

    def __init__(self, unsigned=False, default=None):
        self.unsigned = unsigned
        self.default = default

    definition_f = lambda self: 'TINYINT'
    default_f = lambda self: f'DEFAULT {self.default}' if self.default is not None else ''
    extra_f = lambda self: self.extra + ' UNSIGNED' if self.unsigned else ''


class Boolean(DataType):
    definition = 'TINYINT'

    def __init__(self, default=None):
        if default is not None:
            self.default = self.pre_handling(default)

    def pre_handling(self, value):
        return 1 if value else 0

    def post_handling(self, value):
        return True if value else False

    
    definition_f = lambda self: 'TINYINT(1)'
    default_f = lambda self: f'DEFAULT {self.default}' if self.default is not None else ''
    extra_f = lambda self: self.extra


class Char(DataType):
    definition = 'CHAR'
    def __init__(self, max_length=56, default=None):
        self.max_length = max_length
        self.default = default

    def pre_handling(self, value):
        return f'"{value}"'


    definition_f = lambda self: f'CHAR({self.max_length})'
    default_f = lambda self: f'DEFAULT "{self.default}"' if self.default else ''
    extra_f = lambda self: ''


class VarChar(DataType):
    definition = 'VARCHAR'
    def __init__(self, max_length=56, default=None):
        self.max_length = max_length
        self.default = default

    def pre_handling(self, value):
        return f'"{value}"'


    definition_f = lambda self: f'VARCHAR({self.max_length})'
    default_f = lambda self: f'DEFAULT "{self.default}"' if self.default else ''
    extra_f = lambda self: ''


class DateTime(DataType):
    definition = 'DATETIME'

    def __init__(self, auto_now=None, auto_now_add=None):
        if auto_now_add:
            self.default = 'CURRENT_TIMESTAMP'
        if auto_now:
            self.default = 'CURRENT_TIMESTAMP'
            self.extra = 'ON UPDATE CURRENT_TIMESTAMP'

    def pre_handling(self, value):
        return value.strftime('"%Y-%m-%d %H:%M:%S"')

    
    definition_f = lambda self: 'DATETIME'
    default_f = lambda self: f'DEFAULT {self.default}' if self.default else ''
    extra_f = lambda self: self.extra


class JSON(DataType):
    definition = 'TEXT'
    max_length = 65535

    def pre_handling(self, value):
        return f"'{json.dumps(value)}'"

    def post_handling(self, value):
        if value:
            return json.loads(value)
        else:
            return None

    
    definition_f = lambda self: 'TEXT'
    default_f = lambda self: ''
    extra_f = lambda self: self.extra

        
class LongText(DataType):
    definition = 'LONGTEXT'
    max_length = 4294967295

    definition_f = lambda self: 'LONGTEXT'
    default_f = lambda self: ''
    extra_f = lambda self: self.extra


class MediumText(DataType):
    definition = 'MEDIUMTEXT'
    max_length = 16777215

    definition_f = lambda self: 'MEDIUMTEXT'
    default_f = lambda self: ''
    extra_f = lambda self: self.extra


class Text(DataType):
    definition = 'TEXT'
    max_length = 65535

    definition_f = lambda self: 'TEXT'
    default_f = lambda self: ''
    extra_f = lambda self: self.extra


class TinyText(DataType):
    definition = 'TINYTEXT'
    max_length = 225

    definition_f = lambda self: 'TINYTEXT'
    default_f = lambda self: ''
    extra_f = lambda self: self.extra
    


    


