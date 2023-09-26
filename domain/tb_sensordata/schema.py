# schema.py

from pydantic import BaseModel

class SensorData(BaseModel):
    cSenID: str
    cSenDate: str
    cSenTime: str
    cSenType: str
    cSenAccX: str
    cSenAccY: str
    cSenAccZ: str
    cSenGyrX: str
    cSenGyrY: str
    cSenGyrZ: str
    cSenAngX: str
    cSenAngY: str
    cSenAngZ: str
    cSenTemp: str
    gpsLatitude: str
    gpsLongitude: str
    gpsAltitude: str
    gpsSpeed: str
    movingDistance: int
    datelog: str
    riskChkLevel_1: str
    riskChkLevel_2: str
    cDriverId: str

    class Config:
        orm_mode = True

class TableDate(BaseModel):
    table_date: str

