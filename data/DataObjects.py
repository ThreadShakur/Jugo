import jugo.utils.connection as db
from jugo.utils.exceptions import ItemNotInFieldset

class DataObjects():
    def __init__ (self, model):
        self.model = model
        self.objects = []
        self.idx = -1

    def __iter__ (self):
        return self

    def __getitem__(self, i):
        return self.objects[i]

    def __len__(self):
        return len(self.objects)

    def __next__ (self):
        self.idx += 1

        try:
            return self.objects[self.idx]
        except IndexError:
            raise StopIteration()


    def values(self):
        return self.objects

    def get_fields(self):
        base_fields = self.model.__class__.__base__.__dict__
        own_fields = self.model.__class__.__dict__
        fields = {}

        for item in base_fields:
            if base_fields[item].__class__.__base__.__name__ == 'DataType':
                fields.update({item: base_fields[item]})

        for item in own_fields:
            if own_fields[item].__class__.__base__.__name__ == 'DataType':
                fields.update({item: own_fields[item]})

        return fields

    def update(self, **params):
        fields = self.get_fields()
        fields_keys = fields.keys()
 
        update_query = ''

        for param in params:
            if param == 'id':
                continue

            if param not in fields_keys:
                raise ItemNotInFieldset(param, self.model)

            update_query += f'`{param}` = {fields[param].pre_handling(params[param])}, '

        
        db.cursor.execute(f'UPDATE `{self.model.table_name}` SET {update_query[:-2]} WHERE `id` in ({",".join([str(item.id) for item in self.objects])})')


        

            
            


        
