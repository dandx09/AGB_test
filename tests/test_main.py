import re
import pytest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from database import SessionLocal, engine
from main import app
from models import Analytics, Sales, Base


client = TestClient(app)

# Создание тестовой сессии базы данных
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_parse_sales(monkeypatch):
    def mock_parse_sales_data(*args, **kwargs):
        class MockTask:
            id = "test_task_id"

        return MockTask()

    monkeypatch.setattr("app.tasks.parse_sales_data.delay", mock_parse_sales_data)
    response = client.post("/parse-sales", params={"url": "http://example.com/sales.xml"})
    assert response.status_code == 200
    assert re.match(r"^[a-f0-9\-]{36}$", response.json()["result"]) is not None


# Добавление тестовых данных в базу данных
def test_get_analytics(test_db, monkeypatch):
    new_analytics = Analytics(
        id=1,
        date=datetime(2024, 1, 1),
        analytics="Аналитический отчет по продажам",
    )
    test_db.add(new_analytics)
    test_db.commit()

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    monkeypatch.setattr("app.main.get_db", override_get_db)
    response = client.get("/report?date=2024-01-01")
    assert response.status_code == 200
    analytics = response.json()
    assert analytics["sales_report"] == "Аналитический отчет по продажам"


# Тест вставки данных в базу данных
def test_database_insert(test_db):
    new_sale = Sales(id=3, name="Product C", quantity=30, price=1200.00, category="Furniture")
    test_db.add(new_sale)
    test_db.commit()
    sale = test_db.query(Sales).filter(Sales.id == 3).first()
    assert sale is not None
    assert sale.name == "Product C"
    assert sale.quantity == 30
    assert sale.price == 1200.00
    assert sale.category == "Furniture"


# Тест удаления данных из базы данных
def test_database_delete(test_db):
    sale = test_db.query(Sales).filter(Sales.name == "Product C").first()
    test_db.delete(sale)
    test_db.commit()
    sale = test_db.query(Sales).filter(Sales.name == "Product C").first()
    assert sale is None
