# schema.py
from pydantic import BaseModel
from typing import Optional

class SensorData(BaseModel):
    cSenID: Optional[str]
    cSenDate: Optional[str]
    cSenTime: Optional[str]
    cSenType: Optional[str]
    cSenAccX: Optional[str]
    cSenAccY: Optional[str]
    cSenAccZ: Optional[str]
    cSenGyrX: Optional[str]
    cSenGyrY: Optional[str]
    cSenGyrZ: Optional[str]
    cSenAngX: Optional[str]
    cSenAngY: Optional[str]
    cSenAngZ: Optional[str]
    cSenTemp: Optional[str]
    gpsLatitude: Optional[str]
    gpsLongitude: Optional[str]
    gpsAltitude: Optional[str]
    gpsSpeed: Optional[str]
    movingDistance: Optional[int]
    datelog: Optional[str]
    riskChkLevel_1: Optional[str]
    riskChkLevel_2: Optional[str]
    # cDriverId: str

    @staticmethod
    def from_orm(orm_obj):
        return SensorData(
            cSenID=orm_obj.cSenID if hasattr(orm_obj, 'cSenID') else None,
            cSenDate=orm_obj.cSenDate if hasattr(orm_obj, 'cSenDate') else None,
            cSenTime=orm_obj.cSenTime if hasattr(orm_obj, 'cSenTime') else None,
            cSenType=orm_obj.cSenType if hasattr(orm_obj, 'cSenType') else None,
            cSenAccX=orm_obj.cSenAccX if hasattr(orm_obj, 'cSenAccX') else None,
            cSenAccY=orm_obj.cSenAccY if hasattr(orm_obj, 'cSenAccY') else None,
            cSenAccZ=orm_obj.cSenAccZ if hasattr(orm_obj, 'cSenAccZ') else None,
            cSenGyrX=orm_obj.cSenGyrX if hasattr(orm_obj, 'cSenGyrX') else None,
            cSenGyrY=orm_obj.cSenGyrY if hasattr(orm_obj, 'cSenGyrY') else None,
            cSenGyrZ=orm_obj.cSenGyrZ if hasattr(orm_obj, 'cSenGyrZ') else None,
            cSenAngX=orm_obj.cSenAngX if hasattr(orm_obj, 'cSenAngX') else None,
            cSenAngY=orm_obj.cSenAngY if hasattr(orm_obj, 'cSenAngY') else None,
            cSenAngZ=orm_obj.cSenAngZ if hasattr(orm_obj, 'cSenAngZ') else None,
            cSenTemp=orm_obj.cSenTemp if hasattr(orm_obj, 'cSenTemp') else None,
            gpsLatitude=orm_obj.gpsLatitude if hasattr(orm_obj, 'gpsLatitude') else None,
            gpsLongitude=orm_obj.gpsLongitude if hasattr(orm_obj, 'gpsLongitude') else None,
            gpsAltitude=orm_obj.gpsAltitude if hasattr(orm_obj, 'gpsAltitude') else None,
            gpsSpeed=orm_obj.gpsSpeed if hasattr(orm_obj, 'gpsSpeed') else None,
            movingDistance=orm_obj.movingDistance if hasattr(orm_obj, 'movingDistance') else None,
            datelog=orm_obj.datelog.isoformat() if hasattr(orm_obj, 'datelog') else None,
            riskChkLevel_1=orm_obj.riskChkLevel_1 if hasattr(orm_obj, 'riskChkLevel_1') else None,
            riskChkLevel_2=orm_obj.riskChkLevel_2 if hasattr(orm_obj, 'riskChkLevel_2') else None
            # cDriverId=orm_obj.cDriverId if hasattr(orm_obj, 'cDriverId') else None
        )
    class Config:
        from_attributes = True

class TableDate(BaseModel):
    table_date: str
