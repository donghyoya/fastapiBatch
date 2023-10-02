import os
from dotenv import load_dotenv
import pyodbc
from time import time

# 환경 변수에서 데이터베이스 설정 정보 가져오기
load_dotenv('.env.database')

DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PWD = os.getenv("DATABASE_PWD")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_SERVER = os.getenv("DATABASE_SERVER")

# PyODBC를 사용하여 데이터베이스 연결
connection_string = f"DRIVER={{MariaDB ODBC 3.1 Driver}};SERVER={DATABASE_SERVER};PORT={DATABASE_PORT};DATABASE={DATABASE_DB};USER={DATABASE_USER};PASSWORD={DATABASE_PWD};"
conn = pyodbc.connect(connection_string)

# 테스트 쿼리 실행
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

sql_execute_start = time()
# 쿼리 실행
cursor.execute("SELECT * FROM tb_sensordata_20220409")
results = cursor.fetchall()
sql_execute_end = time()


toList_time_start = time()
# 결과를 리스트로 가져오기
data_list = [row for row in results]
toList_time_end =time()

print(f'pyodbc sql excute time = {sql_execute_end - sql_execute_start}')
print(f'toList time = {toList_time_end - toList_time_start}')
print(f'data length = {len(data_list)}')

cursor.close()
conn.close()
