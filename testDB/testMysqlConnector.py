import mysql.connector
from dotenv import load_dotenv
import os
from time import time

load_dotenv('.env.database')

DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PWD = os.getenv("DATABASE_PWD")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_SERVER = os.getenv("DATABASE_SERVER")

# DB 연결 설정
config = {
  'user': DATABASE_USER,
  'password': DATABASE_PWD,
  'host': DATABASE_SERVER,
  'database': DATABASE_DB,
  'raise_on_warnings': True
}

# DB 연결
connection = mysql.connector.connect(**config)



# 쿼리 실행
sql_time_start = time()
cursor = connection.cursor()
cursor.execute("SELECT * FROM tb_sensordata_20220409")
results = cursor.fetchall()
sql_time_end = time()

# 결과 가져오기
toList_start = time()
data_list = [row for row in results]
toList_end = time()

print(f'msyql connector sql excute time = {sql_time_end - sql_time_start}')
print(f'toList time = {toList_end - toList_start}')

# 리소스 정리
cursor.close()
connection.close()