import logging


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from celery.result import AsyncResult
from database import init_db, get_db
from tasks import parse_sales_data
from models import Analytics

from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Инициализация базы данных
@app.on_event("startup")
def on_startup():
    init_db()  # todo


@app.post("/parse-sales")
async def parse_sales(url: str):
    try:
        logger.info(f"Received request to parse sales from URL: {url}")
        task = parse_sales_data.delay(url)
        logger.info(f"Task {task.id} created for parsing sales data.")
        return {"result": task.id}
    except Exception as e:
        logger.error(f"Error while creating parsing task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/report")
async def get_sales_report(date, db: Session = Depends(get_db)):
    try:
        logger.info(f"Query sales report from {date}")
        query_date = datetime.strptime(date, "%Y-%m-%d")
        results = db.query(Analytics.analytics).filter(Analytics.date == query_date).scalar()
        if results is None:
            logger.warning(f"No results found for date: {date}")
            raise HTTPException(status_code=404, detail="No sales report found for the provided date.")
        return {"sales_report": results}
    except ValueError as ve:
        logger.error(f"Invalid date format: {ve}")
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")
