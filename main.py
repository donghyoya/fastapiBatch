from fastapi import FastAPI
from domain.tb_sensordata.router import router as sensor_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(sensor_router, prefix="/router")
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)