import pymysql
import json

with open('jugo.json', 'r') as f:
    settings = json.load(f)

conn = pymysql.connect(host=settings['host'],
                        user=settings['user'],
                        password=settings['password'],
                        db=settings['db'],
                        autocommit=True,
                        charset=settings['charset'])

cursor = conn.cursor()

