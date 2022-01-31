FROM postgres:12
COPY sql/create_tables.sql /docker-entrypoint-initdb.d/
COPY sql/fill_tables.sql /docker-entrypoint-initdb.d/

FROM python:3.6-slim-buster
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
