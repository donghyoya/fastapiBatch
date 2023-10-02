from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from time import time
from sqlalchemy.sql import text
import os

load_dotenv('.env.database')

username = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PWD")
dbname = os.getenv("DATABASE_DB")
port = os.getenv("DATABASE_PORT")  
host = os.getenv("DATABASE_SERVER") 

DATABASE_URL = f"mysql+mysqldb://{username}:{password}@{host}:{port}/{dbname}?charset=utf8mb4"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

sql_time_start = time()
sql = text(f"SELECT * FROM tb_sensordata_20220409")
db = SessionLocal()
results = db.execute(sql).fetchall()
sql_time_end = time()

toList_start = time()
data_list = [row for row in results]
toList_end = time()

print(f'sqlalchemy sql excute time = {sql_time_end - sql_time_start}')
print(f'toList time = {toList_end - toList_start}')
print(f'data length = {len(data_list)}')
# 리소스 정리
db.close_all()