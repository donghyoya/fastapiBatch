from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class SensorDataTable(Base):
    __tablename__ = 'tb_sensordata_20220211'

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
