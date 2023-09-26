from sqlalchemy.orm import Session
from . import model, schema

def get_data(db: Session, table_date: str, data_id: int):
    table = type("DynamicTable", (model.DynamicTable,), {"table_date": table_date})
    return db.query(table).filter(table.id == data_id).first()

def get_all_data(db: Session, table_date: str):
    table = model.set_dynamic_table(table_date)
    return db.query(table).all()
