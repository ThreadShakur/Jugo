import jugo.utils.connection as db


def get_fields(model):
    base_fields = model.__class__.__base__.__dict__
    own_fields = model.__class__.__dict__
    fields = {}

    for item in base_fields:
        if base_fields[item].__class__.__base__.__name__ == 'DataType':
            fields.update({item: base_fields[item]})

    for item in own_fields:
        if own_fields[item].__class__.__base__.__name__ == 'DataType':
            fields.update({item: own_fields[item]})

    return fields


def get_indexes(model):
    base_fields = model.__class__.__base__.__dict__
    own_fields = model.__class__.__dict__
    indexes = {}


    for item in base_fields:
        if base_fields[item].__class__.__name__ == 'Index':
            indexes.update({item: base_fields[item]})

    for item in own_fields:
        if own_fields[item].__class__.__name__ == 'Index':
            indexes.update({item: own_fields[item]})

    return indexes

def create_table(model):
    # Params of model
    fields = get_fields(model)
    fields_query = ''

    for item in fields:
        datatype = fields[item]

        fields_query += f'`{item}` {datatype.definition_f()} {datatype.default_f()} {datatype.extra_f()}, '

    db.cursor.execute(f'CREATE TABLE `{model.table_name}` ({fields_query[:-2]})  ENGINE=INNODB')


def check_for_changes(model):
    fields = get_fields(model)
    exists_in_table = []

    db.cursor.execute(f'SELECT `COLUMN_NAME`, `COLUMN_DEFAULT`, `DATA_TYPE`, `CHARACTER_MAXIMUM_LENGTH`, `EXTRA`, `COLUMN_KEY`, `COLUMN_TYPE` FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME="{model.table_name}"')
    table_fields = db.cursor.fetchall()

    for table_field in table_fields:
        column_finded = False

        # Iterating params of model, like name, date and etc.
        for param in fields:
            # Finding model param in table schema
            if param == table_field[0]:
                column_finded = True

                exists_in_table.append(param)
                datatype = fields[param]


                # table_field[1] = column default value
                # table_field[2] = column data type
                # table_field[3] = column value max_length
                # table_field[4] = column extra
                # table_field[5] = column key
                # table_field[6] = colunt type
                # If some of this params are not equals, updating table row

                if  (datatype.default != table_field[1] or
                    datatype.definition.lower() != table_field[2] or
                    datatype.max_length != table_field[3] or
                    datatype.extra.lower() != table_field[4].lower() or 
                    (datatype.unsigned and not 'unsigned' in table_field[6]) or
                    (not datatype.unsigned and 'unsigned' in table_field[6])):

                    if table_field[2] in ('int', 'tinyint') and str(datatype.default) == table_field[1]:
                        continue

                    print(f'ALTER field {model.table_name} {param}')

                    db.cursor.execute(f'ALTER TABLE `{model.table_name}` MODIFY COLUMN `{param}` {datatype.definition_f()} {datatype.default_f()} {datatype.extra_f()}')

                break

        # If field is not finded in our model schema - deleting it
        if not column_finded:
            print(f'DROP field {model.table_name} {table_field[0]}')
            db.cursor.execute(f'ALTER TABLE `{model.table_name}` DROP COLUMN `{table_field[0]}`;')

    for param in fields:
        # If field is not exist in table - creating it
        if param not in exists_in_table:
            datatype = fields[param]

            print(f'CREATE field {model.table_name} {param}')
            db.cursor.execute(f'ALTER TABLE `{model.table_name}` ADD `{param}` {datatype.definition_f()} {datatype.default_f()} {datatype.extra_f()}')

    # db.cursor.execute(f'SELECT `INDEX_NAME`, `COLUMN_NAME` FROM INFORMATION_SCHEMA.STATISTICS WHERE `TABLE_NAME` = "{model.table_name}" AND `TABLE_SCHEMA` = "{db.settings["db"]}"')
    # index_fields = db.cursor.fetchall()

    # indexes = get_indexes(model)
    # for index_field in index_fields:
    # for index in indexes:
    #     print(f'CREATE INDEX `{index}` ON `{model.table_name}` ({",".join([item for item in indexes[index].fields])});')
    #     db.cursor.execute(f'CREATE INDEX `{index}` ON `{model.table_name}` ({",".join([item for item in indexes[index].fields])});')


def syncdb(models):
    db.cursor.execute(f'SELECT `TABLE_NAME` FROM INFORMATION_SCHEMA.TABLES WHERE `TABLE_SCHEMA` = "{db.settings["db"]}"')

    tables = [item[0] for item in db.cursor.fetchall()]

    exist_tables = []
    models = __import__(models).__dict__

    for model in models:
        if '__call__' in models[model].__class__.__dict__.keys() and model != 'Model':
            item = models[model].__call__()

            if item.__class__.__base__.__name__ == 'Model':
                exist_tables.append(item.table_name)
                if item.table_name not in tables:
                    create_table(item)
                else:
                    check_for_changes(item)
    
    for table in tables:
        if table not in exist_tables:
            print(f'DROP table {table}')
            db.cursor.execute(f'DROP TABLE `{table}`')


                
