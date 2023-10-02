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

@router.get("/getData",response_model=int) #List[schema.SensorData]
def get_tb_sensorData(table_date: str = Query(
    default="20220409", 
    example="20220409"
),db:Session = Depends(get_db)):
    # sensor_db = crud.get_test_all_data(table_date=table_date,db=db)
    count = crud.get_data_count(table_date=table_date,db=db)
    sensor_db_old = crud.get_all_data_raw_sql(table_date=table_date, db=db)
    # sensor_db = crud.get_test_all_data(table_date=table_date,db=db)
    print(f'length data {table_date} = {len(sensor_db_old)}')
    return count
