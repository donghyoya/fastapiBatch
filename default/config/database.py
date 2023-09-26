from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# DATABASE_URL = "mysql+mysqldb://<username>:<password>@<host>/<dbname>?charset=utf8mb4"

load_dotenv('.env.database')

username = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PWD")
dbname = os.getenv("DATABASE_DB")
port = os.getenv("DATABASE_PORT")  
host = os.getenv("DATABASE_SERVER") 

# DATABASE_URL = "mysql+mysqldb://"+username+":"+password+"@"+server+":"+host+"/"+dbname+"?charset=utf8mb4"
DATABASE_URL = f"mysql+mysqldb://{username}:{password}@{host}:{port}/{dbname}?charset=utf8mb4"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
