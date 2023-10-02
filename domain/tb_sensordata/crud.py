from sqlalchemy.orm import Session
from . import model, schema, tb_model
from sqlalchemy.sql import text
from typing import List
from time import time
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor

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

def get_test_all_data(db: Session, table_date: str):
    table = model.set_dynamic_table(table_date=table_date)
    results = db.query(table).all()
    print("=================================================")
    data_list = [row for row in results]
    # response_data = [schema.SensorData.from_orm(item) for item in data]
    return data_list

def get_data_count(db: Session, table_date: str) -> int:
    table = model.set_dynamic_table(table_date)
    count = db.query(table).count()
    print("=================================================")
    return count


def get_all_data_raw_sql(db: Session, table_date: str):
    table_name = f"tb_sensordata_{table_date}"
    sql = text(f"SELECT * FROM {table_name}")
    start_execute_time = time()
    # DB 연결과 multiprocessing 은 사용이 안됀다
    # with Pool(processes=16) as pool:
    #     result = pool.map(db.execute,sql)
    execute_time_start = time()
    results = db.execute(sql).fetchall()
    execute_time_end = time()

    toList_start = time()
    data_list = [row for row in results]
    toList_end = time()

    print(f'sql execute time: {execute_time_end - execute_time_start}')
    print(f'toList time: {toList_end - toList_start}')
    print(f'data list 1 length: {len(data_list)}')
    return data_list


def __change_SensorData_List(row):
    
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
    return data

'''
    end_execute_time = time()

    start_row_change_time = time()
    with Pool(processes=12) as pool:
      data_list = pool.map(__change_SensorData_List, result)
    # data_list = __change_SensorData_List(result=result)
    end_raw_change_time = time()

    start_row_change_time2 = time()
    with ThreadPoolExecutor(max_workers=12) as executor:
      data_list2 = list(executor.map(__change_SensorData_List, result))
    # data_list = __change_SensorData_List(result=result)
    end_raw_change_time2 = time()

    print(f'sqlalchemy execute spend time : {end_execute_time - start_execute_time}')
    print(f'raw change spend time: {end_raw_change_time-start_row_change_time}')
    print(f'raw change2 spend time: {end_raw_change_time2-start_row_change_time2}')
    print(f'data_list1 = {len(data_list)}, data_list2 = {len(data_list2)}')
    #return result.fetchall()
'''