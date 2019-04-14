import jugo.utils.connection as db

class DataObject():
    def __init__(self, table_name):
        self.__tablename__ = table_name

    def save(self, update_fields=None):
        fields = self.__dict__
        update_query = ''

        for param in fields:
            if fields[param].__class__.__base__.__name__ == 'DataType' or param == 'id' or param == '__tablename__' or (update_fields and param not in update_fields):
                continue

            value = fields[f"{param}__datatype__"].pre_handling(fields[param])

            update_query += f'`{param}` = {value if value is not None else "NULL"}, '

        print(update_query)
        db.cursor.execute(f'UPDATE `{self.__tablename__}` SET {update_query[:-2]} WHERE `id` = {fields["id"]}')

            
