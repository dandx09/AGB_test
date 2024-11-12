import logging

import openai
import requests
import xml.etree.ElementTree as ET

from datetime import datetime
from models import Sales
from config import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_xml(url):
    logger.info(f"Downloading XML data from URL: {url}")
    response = requests.get(url)
    response.raise_for_status()
    logger.info("XML data downloaded successfully.")
    return response.text


def parse_xml_to_db(xml_data) -> list[Sales]:
    logger.info("Parsing XML data to database format.")
    root = ET.fromstring(xml_data)
    sales_data: list[Sales] = []
    date: datetime = datetime.strptime(
        root.attrib.get("date"), "%Y-%m-%d"
    )  # todo добавить обработку ошибки, если нет даты
    for product in root.find("products"):
        sales_record = Sales(
            product_id=int(product.find("id").text),
            date=date,
            name=product.find("name").text,
            quantity=int(product.find("quantity").text),
            price=float(product.find("price").text),
            category=product.find("category").text,
        )
        sales_data.append(sales_record)
    logger.info("XML data parsed successfully.")
    return sales_data


def row_to_dict(row):
    return {
        "product_id": row.product_id,
        "date": row.date,
        "name": row.name,
        "quantity": row.quantity,
        "price": row.price,
        "category": row.category,
    }


def generate_prompt(sales_data) -> []:
    logger.info("Start generating prompt to LLM")
    sales_records = [row_to_dict(row) for row in sales_data]
    current_date = sales_records[0]["date"]
    total_revenue = sum(sale["quantity"] * sale["price"] for sale in sales_records)
    top_products = sorted(sales_records, key=lambda x: x["quantity"], reverse=True)[:3]
    categories = {}
    for sale in sales_records:
        if sale["category"] in categories:
            categories[sale["category"]] += sale["quantity"] * sale["price"]
        else:
            categories[sale["category"]] = sale["quantity"] * sale["price"]
    categories_distribution = {k: f"{v / total_revenue:.2%}" for k, v in categories.items()}
    openai_query: str = f"""
    Проанализируй следующие данные о продажах за дату {current_date.strftime('%Y-%m-%d')}:
    
    Общая выручка: {total_revenue}
    
    Топ-3 товара по продажам: {[
            {"name": product['name'], "quantity": product['quantity'],
             "revenue": product['quantity'] * product['price']}
            for product in top_products
        ]}
    
    Распределение по категориям: {categories_distribution}
    
    Все проданные товары за этот день: {sales_records}

Составь подробный аналитический отчет с выводами и рекомендациями, включая:
    - Общую выручку за период.
    - Топ-3 самых продаваемых товаров и их вклад в выручку.
    - Анализ распределения продаж по категориям и выявление сильных и слабых сегментов.
    - Рекомендации по повышению продаж в слабо развитых категориях.
    - Идентификацию товаров, демонстрирующих потенциал роста, и предложения по усилению их продвижения.
    - Советы по улучшению ассортимента, включая добавление востребованных товаров и исключение товаров с низкой рентабельностью.
    - Оптимизация ценовой стратегии для увеличения прибыли.
    - Идеи для проведения акций и специальных предложений для увеличения объема продаж.
    - Стратегии для учета сезонности и рыночных трендов для максимизации дохода.
    """
    logger.info("Generating prompt to LLM successfully")
    result = [openai_query, current_date]
    return result


def analyze_with_llm(prompt):
    logger.info("Start sent prompt to LLM.")
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": " Ты — менеджер по продажам в крупнейшей компании мира, специализирующейся на розничной торговле. Твоя задача — анализировать продажи и находить возможности для улучшения стратегий, чтобы обеспечить устойчивый рост компании и увеличить прибыль.",
                },
                {"role": "user", "content": prompt},
            ],
            model="gpt-4o",
            max_tokens=1000,
        )
        analysis = chat_completion.choices[0].message.content
        logger.info("Prompt sent to LLM successfully.")
        return analysis
    except Exception as e:
        logger.error(f"Error while sending prompt to LLM: {e}")
        raise Exception("No sales report found for the provided date.")
