import os
import configparser
import socket


parser = configparser.ConfigParser()
parser.read("env.txt")

POSTGRESQL_ADDRESS = os.getenv('POSTGRESQL_ADDRESS') or parser.get("config", "POSTGRESQL_ADDRESS")
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME') or parser.get("config", "POSTGRESQL_USERNAME")
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD') or parser.get("config", "POSTGRESQL_PASSWORD")
POSTGRESQL_DATABASE_NAME = os.getenv('POSTGRESQL_DATABASE_NAME') or parser.get("config", "POSTGRESQL_DATABASE_NAME")
TABLE_NAME = os.getenv('POSTGRESQL_TABLE_NAME') or parser.get("config", "POSTGRESQL_TABLE_NAME")
DATABASE_URL = 'postgresql://' + POSTGRESQL_USERNAME + ':' + POSTGRESQL_PASSWORD + '@' + POSTGRESQL_ADDRESS + \
               '/' + POSTGRESQL_DATABASE_NAME
WEBSERVER_DIR = os.getenv('WEBSERVER_DIR')
WEBSERVER_URL = os.environ.get('WEBSERVER_URL')
RESTAPI_URL = os.environ.get('RESTAPI_URL') or parser.get("config", "RESTAPI_URL")
RESTAPI_PORT = int(os.environ.get('RESTAPI_PORT') or parser.get("config", "RESTAPI_PORT"))
TOKEN_SECRET = os.environ.get('TOKEN_SECRET') or parser.get("config", "TOKEN_SECRET")
HOSTNAME = socket.gethostname()
