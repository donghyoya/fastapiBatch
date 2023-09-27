from sqlalchemy.orm import Session
from . import model, schema
from sqlalchemy.sql import text

def get_data(db: Session, table_date: str, data_id: int):
    table = type("DynamicTable", (model.DynamicTable,), {"table_date": table_date})
    return db.query(table).filter(table.id == data_id).first()

def get_all_data(db: Session, table_date: str):
    table = model.set_dynamic_table(table_date)
    data = db.query(table).all()
    print(f'crud data = {data}')
    response_data = [schema.SensorData.from_orm(item) for item in data]
    return response_data

def get_data_count(db: Session, table_date: str):
    table = model.set_dynamic_table(table_date)
    return db.query(table).count()

def get_all_data_raw_sql(db: Session, table_date: str):
    table_name = f"tb_sensordata_{table_date}"
    sql = text(f"SELECT * FROM {table_name}")
    result = db.execute(sql)
    data_list = []
    for row in result:
        data = schema.SensorData(
            cSenID=row.cSenID,
            cSenDate=row.cSenDate,
            cSenTime=row.cSenTime,
            cSenType=row.cSenType,
            cSenAccX=row.cSenAccX,
            cSenAccY=row.cSenAccY,
            cSenAccZ=row.cSenAccZ,
            cSenGyrX=row.cSenGyrX,
            cSenGyrY=row.cSenGyrY,
            cSenGyrZ=row.cSenGyrZ,
            cSenAngX=row.cSenAngX,
            cSenAngY=row.cSenAngY,
            cSenAngZ=row.cSenAngZ,
            cSenTemp=row.cSenTemp,
            gpsLatitude=row.gpsLatitude,
            gpsLongitude=row.gpsLongitude,
            gpsAltitude=row.gpsAltitude,
            gpsSpeed=row.gpsSpeed,
            movingDistance=row.movingDistance,
            datelog=row.datelog.isoformat(),
            riskChkLevel_1=row.riskChkLevel_1,
            riskChkLevel_2=row.riskChkLevel_2
            # cDriverId=row.cDriverId (필요하다면 이 부분도 추가)
        )
        data_list.append(data)
    #return result.fetchall()
    return data_list






    