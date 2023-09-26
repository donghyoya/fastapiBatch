from fastapi import FastAPI
from domain.tb_sensordata.router import router as sensor_router

app = FastAPI()

app.include_router(sensor_router, prefix="/router")