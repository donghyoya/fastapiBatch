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
def get_database():
    connection = mysql.connector.connect(**config)
    return connection