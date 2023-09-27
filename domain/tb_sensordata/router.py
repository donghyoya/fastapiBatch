from fastapi import APIRouter, Depends, HTTPException, Query
from . import crud, schema
from sqlalchemy.orm import  Session
from default.config import database
from typing import List

router = APIRouter(
    tags=["tb_sensor"]
)

def get_db():
    try:
        db=database.SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/getData",response_model=List[schema.SensorData])
def get_tb_sensorData(table_date: str = Query(
    default="20220211", 
    example="20220211"
),db:Session = Depends(get_db)):
    sensor_db = crud.get_all_data(table_date=table_date,db=db)
    sensor_db2 = crud.get_all_data_raw_sql(table_date=table_date,db=db)
    # 데이터 개수 로깅
    data_count = crud.get_data_count(table_date=table_date, db=db)

    print(f'Total data length in sensor_db : {len(sensor_db)}')
    print(f'Total data length in sensor_db2 : {len(sensor_db2)}')
    print(f"Total data count in table {table_date}: {data_count}")

    return sensor_db
