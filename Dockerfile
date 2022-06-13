FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV POSTGRESQL_ADDRESS="95.181.161.40"
ENV POSTGRESQL_USERNAME="nokia"
ENV POSTGRESQL_PASSWORD="Nira1256#"
ENV POSTGRESQL_DATABASE_NAME="Nokia"
ENV POSTGRESQL_TABLE_NAME="foodlist"
ENV RESTAPI_URL=0.0.0.0
ENV RESTAPI_PORT=8000

CMD [ "python", "./main.py" ]
