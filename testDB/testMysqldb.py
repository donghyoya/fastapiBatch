import MySQLdb
from dotenv import load_dotenv
import os
from time import time

load_dotenv('.env.database')

DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PWD = os.getenv("DATABASE_PWD")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_SERVER = os.getenv("DATABASE_SERVER")

conn = MySQLdb.connect(host=DATABASE_SERVER, user=DATABASE_USER, passwd=DATABASE_PWD, db=DATABASE_DB, port=DATABASE_PORT)

sql_time_start = time()
cursor = conn.cursor()
cursor.execute("SELECT * FROM tb_sensordata_20220409")
sql_time_end = time()

toList_start = time()
results = cursor.fetchall()
data_list = [row for row in results]
toList_end = time()


print(f'sqlalchemy sql excute time = {sql_time_end - sql_time_start}')
print(f'toList time = {toList_end - toList_start}')
print(f'data length = {len(data_list)}')
cursor.close()
conn.close()