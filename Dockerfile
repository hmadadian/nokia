FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV POSTGRESQL_ADDRESS="test"
ENV POSTGRESQL_USERNAME="postgres"
ENV POSTGRESQL_PASSWORD="test"
ENV POSTGRESQL_DATABASE_NAME="nokia_test"
ENV POSTGRESQL_TABLE_NAME="foodlist"
ENV RESTAPI_URL=0.0.0.0
ENV RESTAPI_PORT=8000

CMD [ "python", "./main.py" ]
