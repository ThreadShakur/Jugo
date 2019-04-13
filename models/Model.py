from jugo.data.DataObjects import DataObjects
from jugo.data.DataObject import DataObject
from jugo.models import types
from jugo.utils.exceptions import ItemNotInFieldset, UsedReservedVariable
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


    def objects(self, **params):
        fields = self.get_fields()
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


        if params:
            where_query = 'WHERE '
            for index, item in enumerate(params):
                if item not in fields_keys:
                    raise ItemNotInFieldset(item, self)

                if index == len(params) - 1:
                    where_query += f'`{item}` = {fields[item].pre_handling(params[item])}'
                else:
                    where_query += f'`{item}` = {fields[item].pre_handling(params[item])} AND '


        self.cursor.execute(f'SELECT {select_query if select_query else "*"} FROM `{self.table_name}` {where_query} {order_by_query[:-2]} {"LIMIT %d" % limit if limit else ""}')
        data = self.cursor.fetchall()


        data_objects = DataObjects(self)
        for field in data:
            obj = DataObject(self.table_name)
            for param in field:
                setattr(obj, param, fields[param].post_handling(field[param]))
                setattr(obj, f'{param}__datatype__', fields[param])

            data_objects.objects.append(obj)

        return data_objects
            

