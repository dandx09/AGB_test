### Архитектура решения:

1. **FastAPI Сервис**:
   - REST API на базе FastAPI с точками входа для обработки XML данных (`/parse-sales`), получения аналитических отчетов (`/report`).

2. **Парсинг XML**:
   - Использование `xml.etree.ElementTree` для парсинга данных о продуктах из XML, полученного через HTTP-запрос.

3. **Хранилище данных**:
   - PostgreSQL для хранения данных.
   - SQLAlchemy для ORM и безопасного доступа к базе данных.

4. **Запланированные задачи**:
   - Celery для ежедневного скачивания и обработки XML файлов, с Redis в качестве брокера задач.

5. **Обработка и Анализ с LLM**:
   - Формирование промпта с данными для анализа продаж, отправка в LLM (OpenAI) и сохранение ответа в базу данных.

6. **Докеризация**:
   - Dockerfile и Docker-compose для контейнеризации компонентов сервиса (FastAPI, PostgreSQL, Celery, Redis).

7. **Логирование и мониторинг**:
   - Логирование операций с помощью `logging`.

8. **Тестирование**:
   - Unit-тесты для основных функций с использованием `pytest`.

### Пример сгенерированного отчёта:
```llm_responce
Аналитический отчет по продажам за 2024-01-01
1. Общая выручка за период
Общая выручка компании за 1 января 2024 года составила 555,250.0.

2. Топ-3 самых продаваемых товаров и их вклад в выручку
Product D: Продано 200 единиц, выручка — 20,000.0. Вклад в общую выручку: 3.6%.
Product E: Продано 120 единиц, выручка — 144,000.0. Вклад в общую выручку: 25.9%.
Product I: Продано 110 единиц, выручка — 16,500.0. Вклад в общую выручку: 3.0%.
Вывод: Товар Product E является лидером по выручке и продажам, что подчеркивает его высокую популярность и рентабельность.

3. Анализ распределения продаж по категориям
Electronics: 60.65% от общей выручки — основной сегмент продаж.
Luxury Goods: 10.81% — значительная часть выручки, указывающая на высокий спрос на премиальные товары.
Sports Equipment: 8.10% — стабильный вклад в общий объем продаж.
Furniture: 6.75% — умеренный сегмент, возможно, нуждается в улучшении стратегии.
Остальные категории (Stationery, Clothing, Books, Home Appliances): вносят менее 5% каждая, что указывает на их низкий потенциал или недостаточное продвижение.
Вывод: Категория Electronics доминирует, что указывает на высокий спрос и широкую линейку востребованных товаров. Однако категории Home Appliances, Stationery, и Books требуют дополнительного внимания и усилий по продвижению.

4. Рекомендации по повышению продаж в слабо развитых категориях
Stationery и Books: Проведение специальных акций, таких как скидки или наборы из популярных товаров, чтобы увеличить внимание к этим сегментам.
Home Appliances: Поддержка рекламных кампаний с демонстрацией полезных функций и преимуществ продукции.
Furniture: Увеличение ассортимента путем добавления многофункциональных или компактных решений для современных жилищ.
5. Идентификация товаров с потенциалом роста и предложения по усилению их продвижения
Product I (категория: Books) показывает хорошие объемы продаж, но относительно низкую выручку. Увеличение ценности предложения, например, путем добавления эксклюзивных комплектов книг или авторских изданий, может повысить спрос и прибыль.

Product G (Sports Equipment) имеет умеренные показатели, но может стать более популярным при проведении маркетинговых акций и выделении сезонных трендов (например, спортивные мероприятия).

6. Советы по улучшению ассортимента
Добавление востребованных товаров: Увеличить предложение в категории Electronics, включая новинки и гаджеты.
Исключение товаров с низкой рентабельностью: Пересмотреть товарные позиции в категориях Stationery и Home Appliances для оптимизации склада и ассортимента.
7. Оптимизация ценовой стратегии для увеличения прибыли
Проведение анализа ценовой чувствительности в категории Clothing и Books. Введение динамического ценообразования для увеличения продаж при снижении цены в определенные периоды.
Пересмотр ценовой стратегии на высокоприбыльные товары, такие как Luxury Goods, с целью определения оптимальной ценовой точки.
8. Идеи для проведения акций и специальных предложений
Кросс-продажи: Комплекты товаров из категорий Electronics и Furniture.
Сезонные скидки: Организация распродаж в категории Clothing для повышения оборота.
Эксклюзивные предложения: Бонусы при покупке товаров из категории Sports Equipment, привязанные к популярным спортивным событиям.
9. Стратегии учета сезонности и рыночных трендов
Сезонные акции для повышения спроса: Организация специальных предложений для Luxury Goods и Sports Equipment во время праздников или крупных спортивных событий.
Анализ трендов: Регулярный мониторинг рыночных трендов в категории Electronics, включая новинки и инновации.
Заключение: Компания должна сосредоточить внимание на развитии категорий с высоким потенциалом роста и улучшении ассортиментной стратегии в слаборазвитых сегментах. Специальные акции, корректировка ценовой политики и укрепление позиций ключевых категорий позволят увеличить выручку и удержать лидирующие позиции на рынке.
```

Использованные для этого ответа данные о продажах:
```xml
<sales_data date="2024-01-01">
    <products>
        <product>
            <id>1</id>
            <name>Product A</name>
            <quantity>100</quantity>
            <price>1500.00</price>
            <category>Electronics</category>
        </product>
        <product>
            <id>2</id>
            <name>Product B</name>
            <quantity>50</quantity>
            <price>250.00</price>
            <category>Home Appliances</category>
        </product>
        <product>
            <id>3</id>
            <name>Product C</name>
            <quantity>75</quantity>
            <price>500.00</price>
            <category>Furniture</category>
        </product>
        <product>
            <id>4</id>
            <name>Product D</name>
            <quantity>200</quantity>
            <price>100.00</price>
            <category>Stationery</category>
        </product>
        <product>
            <id>5</id>
            <name>Product E</name>
            <quantity>120</quantity>
            <price>1200.00</price>
            <category>Electronics</category>
        </product>
        <product>
            <id>6</id>
            <name>Product F</name>
            <quantity>90</quantity>
            <price>300.00</price>
            <category>Clothing</category>
        </product>
        <product>
            <id>7</id>
            <name>Product G</name>
            <quantity>60</quantity>
            <price>750.00</price>
            <category>Sports Equipment</category>
        </product>
        <product>
            <id>8</id>
            <name>Product H</name>
            <quantity>30</quantity>
            <price>2000.00</price>
            <category>Luxury Goods</category>
        </product>
        <product>
            <id>9</id>
            <name>Product I</name>
            <quantity>110</quantity>
            <price>150.00</price>
            <category>Books</category>
        </product>
        <product>
            <id>10</id>
            <name>Product J</name>
            <quantity>45</quantity>
            <price>950.00</price>
            <category>Electronics</category>
        </product>
    </products>
</sales_data>
```

### Запуск проекта

#### Предварительные требования:
- Установленный Docker и Docker Compose.
- Python 3.12 и Poetry для локального тестирования и разработки.
- Переменные окружения для настроек.

#### Шаги для запуска:

1. **Клонирование репозитория**:
   ```bash
   git clone https://github.com/dandx09/AGB_test
   cd AGB_test/
   ```

2. **Настройка переменных окружения**:
   Создайте файл `.env` в корне проекта и укажите необходимые переменные окружения. Пример:
   ```env
   DATABASE_URL=postgresql+psycopg2://user:password@db:5432/sales
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=sales
   CELERY_BROKER_URL=redis://redis:6379/0
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Запуск через Docker Compose**:
   Выполните следующую команду, чтобы запустить все компоненты с помощью Docker Compose:
   ```bash
   docker-compose up --build
   ```
   Это запустит контейнеры для FastAPI сервиса, PostgreSQL базы данных, Redis и Celery воркеров.

4. **Документация API**:
   После запуска сервиса, документацию API можно найти по следующему URL:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

5. **Запуск тестов**:
   Для запуска тестов, выполните следующую команду:
   ```bash
   poetry install --with dev
   pytest tests/
   ```

6. **Мониторинг и Логирование**:
   Логи сервиса можно посмотреть с помощью Docker:
     ```bash
     docker-compose logs -f
     ```

7. **Остановка всех сервисов**:
   Чтобы остановить все контейнеры, выполните команду:
   ```bash
   docker-compose down
   ```