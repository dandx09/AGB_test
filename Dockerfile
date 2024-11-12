FROM python:3.12.7-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry &&  \
    poetry config virtualenvs.create false &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.pyenv/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY ./app /app

EXPOSE 8000
