from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import MetaData
from sqlalchemy import create_engine, Column, Integer, String, DateTime

Base = declarative_base()

class DynamicTable:
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return f'tb_sensordata_{cls.table_date}'

    cSenID = Column(String(20), primary_key=True, index=True)
    cSenDate = Column(String(20))
    cSenTime = Column(String(20))
    cSenType = Column(String(10))
    cSenAccX = Column(String(20))
    cSenAccY = Column(String(20))
    cSenAccZ = Column(String(20))
    cSenGyrX = Column(String(20))
    cSenGyrY = Column(String(20))
    cSenGyrZ = Column(String(20))
    cSenAngX = Column(String(20))
    cSenAngY = Column(String(20))
    cSenAngZ = Column(String(20))
    cSenTemp = Column(String(10))
    gpsLatitude = Column(String(20))
    gpsLongitude = Column(String(20))
    gpsAltitude = Column(String(20))
    gpsSpeed = Column(String(20))
    movingDistance = Column(Integer)
    datelog = Column(DateTime)
    riskChkLevel_1 = Column(String(10))
    riskChkLevel_2 = Column(String(10))
    # cDriverId = Column(String(100))


    def __init__(self, table_date):
        self.table_date = table_date

def set_dynamic_table(table_date: str):
    Base = declarative_base(metadata=MetaData())
    return type("DynamicTable", (Base, DynamicTable), {"table_date": table_date})