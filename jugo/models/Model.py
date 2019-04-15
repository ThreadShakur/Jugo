from jugo.data.DataObjects import DataObjects
from jugo.data.DataObject import DataObject
from jugo.models import types
from jugo.utils.exceptions import ItemNotInFieldset, UsedReservedVariable, UsedExceptedSymbol
import jugo.utils.connection as db
import pymysql

RESERVED_VARS = ('id', 'j_select', 'j_limit', 'j_order')

class Model:
    id = types.Integer(auto_increment=True)

    def __str__(self):
        return self.__class__.__name__

    def __init__(self):
        self.table_name = self.__str__().lower()
        self.cursor  = db.conn.cursor(pymysql.cursors.DictCursor)

        for field in self.get_fields(only_own=True).keys():
            if field in RESERVED_VARS:
                raise UsedReservedVariable(field, self)

            if '__' in field:
                raise UsedExceptedSymbol(field, self)


    def get_fields(self, only_own=False, only_base=False):
        base_fields = self.__class__.__base__.__dict__
        own_fields = self.__class__.__dict__
        fields = {}

        if only_own: base_fields = []
        if only_base: own_fields = []
        
    
        for item in base_fields:
            if base_fields[item].__class__.__base__.__name__ == 'DataType':
                fields.update({item: base_fields[item]})

        for item in own_fields:
            if own_fields[item].__class__.__base__.__name__ == 'DataType':
                fields.update({item: own_fields[item]})

        return fields


    def create(self, **params):
        fields = self.get_fields()
        fields_keys = fields.keys()

        create_query = ''

        for param in params:
            if param not in fields_keys:
                raise ItemNotInFieldset(param, self)

            if param == 'id':
                continue

            create_query += f'`{param}` = {fields[param].pre_handling(params[param])}, '


        db.cursor.execute(f'INSERT INTO `{self.table_name}` SET {create_query[:-2]}')


    def query_builder(self, params, fields):
        fields_keys = fields.keys()

        select = []
        limit = None
        order_by = None

        if params.get('j_select'):
            select = params.pop('j_select')
            if not 'id' in select:
                select.append('id')

        if params.get('j_limit'):
            limit = params.pop('j_limit')

        if params.get('j_order'):
            order_by = params.pop('j_order')

        select_query = ','.join([f'`{item}`' for item in select])
        order_by_query = ''
        where_query = ''

        if order_by:
            order_by_query = 'ORDER BY '
            for item in order_by:
                if item[0] == '-':
                    order_by_query += f'`{item[1:]}` DESC, '
                else:
                    order_by_query += f'`{item}` ASC, '

            order_by_query = order_by_query[:-2]


        if params:
            where_query = 'WHERE '
            for index, item in enumerate(params):
                digit = '='
                value = params[item]
                command = item.split('__')[-1]
                item = item.split('__')[0]


                if command == 'gt':
                    digit = '>'

                elif command == 'egt':
                    digit = '>='

                elif command == 'elt':
                    digit = '<='

                elif command == 'lt':
                    digit = '<'

                elif command == 'not':
                    digit = '<>'

                elif command == 'like':
                    digit = 'LIKE'

                elif command == 'in':
                    digit = 'IN'

                elif command == 'notin':
                    digit = 'NOT IN'

                if item not in fields_keys:
                    raise ItemNotInFieldset(item, self)


                if digit == 'IN' or digit == 'NOT IN':
                    where_query += f'`{item}` {digit} ({",".join([str(fields[item].pre_handling(data)) for data in value]) })'
                else:
                    where_query += f'`{item}` {digit} {fields[item].pre_handling(value)}'

                if index != len(params) - 1:
                    where_query += ' AND '

        return select_query, where_query, order_by_query, limit

    
    def objects(self, **params):
        fields = self.get_fields()
        select_query, where_query, order_by_query, limit = self.query_builder(params, fields)

        self.cursor.execute(f'SELECT {select_query if select_query else "*"} FROM `{self.table_name}` {where_query} {order_by_query} {"LIMIT %d" % limit if limit else ""}')
        data = self.cursor.fetchall()


        data_objects = DataObjects(self)
        for field in data:
            obj = DataObject(self.table_name)
            for param in field:
                setattr(obj, param, fields[param].post_handling(field[param]))
                setattr(obj, f'{param}__datatype__', fields[param])

            data_objects.objects.append(obj)

        return data_objects


    def count(self, **params):
        fields = self.get_fields()
        select_query, where_query, order_by_query, limit = self.query_builder(params, fields)
        
        self.cursor.execute(f'SELECT COUNT(*) AS `count` FROM `{self.table_name}` {where_query} {order_by_query} {"LIMIT %d" % limit if limit else ""}')
        return self.cursor.fetchone()['count']

            

