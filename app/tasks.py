import logging
from celery import Celery
from utils import download_xml, parse_xml_to_db, generate_prompt, analyze_with_llm
from database import SessionLocal
from config import CELERY_BROKER_URL
from models import Analytics


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery(
    "tasks", broker=CELERY_BROKER_URL
)


@celery_app.task
def parse_sales_data(url):
    try:
        logger.info(f"Starting to parse sales data from URL: {url}")
        xml_data = download_xml(url)
        sales_data = parse_xml_to_db(xml_data)
        prompt = generate_prompt(sales_data)
        llm_response = analyze_with_llm(prompt[0])
        db = SessionLocal()
        try:
            db.add(Analytics(date=prompt[1], analytics=llm_response))
            db.bulk_save_objects(sales_data)
            db.commit()
            logger.info("Sales and llm_response saved to database successfully.")

        finally:
            db.close()
            logger.info("Database session closed after saving sales data.")
    except Exception as e:
        logger.error(f"Error while parsing sales data: {e}")
