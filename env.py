import os

POSTGRESQL_ADDRESS = os.getenv('POSTGRESQL_ADDRESS')
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_DATABASE_NAME = os.getenv('POSTGRESQL_DATABASE_NAME')
TABLE_NAME = os.getenv('POSTGRESQL_TABLE_NAME')
DATABASE_URL = 'postgresql://' + POSTGRESQL_USERNAME + ':' + POSTGRESQL_PASSWORD + '@' + POSTGRESQL_ADDRESS + \
               '/' + POSTGRESQL_DATABASE_NAME
WEBSERVER_DIR = os.getenv('WEBSERVER_DIR')
WEBSERVER_URL = os.environ.get('WEBSERVER_URL')
