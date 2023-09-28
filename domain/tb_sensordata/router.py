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
    sensor_db = crud.get_test_all_data(table_date=table_date,db=db)
    print(f'length data 20220211 = {len(sensor_db)}')
    return sensor_db
