from sqlalchemy.orm import Session
from . import model, schema, tb_model
from sqlalchemy.sql import text
from typing import List

def get_data(db: Session, table_date: str, data_id: int):
    table = type("DynamicTable", (model.DynamicTable,), {"table_date": table_date})
    return db.query(table).filter(table.id == data_id).first()

def get_all_data(db: Session, table_date: str):
    table = model.set_dynamic_table(table_date)
    data = db.query(table).all()
    query = db.query(table)
    querydata = query.offset(0).limit(20).all()
    # querydata2 = query.page(2,per_page=20).all()
    print(f'str query = {str(query)}')
    print(f'str query all = {str(querydata)}')
    print(f'str query all = {len(querydata)}')
    # print(f'str query all2 = {str(querydata2)}')
    # print(f'str query all2 = {len(querydata2)}')
    print(f'crud data length = {len(data)}')
    print(f'crud data type = {type(data)}')
    response_data = [schema.SensorData.from_orm(item) for item in data]
    single_result = data[0]
    convert_data = schema.SensorData.from_orm(single_result)
    print(f'converted_data = {convert_data}')
    return response_data

def get_test_all_data(db: Session, table_date: str) -> List[schema.SensorData]:
    data = db.query(tb_model.SensorDataTable).all()
    print("=================================================")
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






    