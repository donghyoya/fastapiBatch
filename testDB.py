from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv('.env.database')

username = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PWD")
dbname = os.getenv("DATABASE_DB")
port = os.getenv("DATABASE_PORT")  
host = os.getenv("DATABASE_SERVER") 

DATABASE_URL = f"mysql+mysqldb://{username}:{password}{host}:{port}/{dbname}?charset=utf8mb4"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def test_database_connection():
    try:
        # 연결 시도
        connection = engine.connect()
        print("데이터베이스에 성공적으로 연결되었습니다!")
        connection.close()
    except exc.SQLAlchemyError as e:
        print(f"데이터베이스 연결에 실패했습니다. 오류: {e}")


if __name__ == "__main__":
    test_database_connection()
