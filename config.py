import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB_NAME = os.getenv('MYSQL_DB_NAME')
CLOUDE_MODEL = os.getenv('CLOUDE_MODEL')
CLOUDE_API_KEY = os.getenv('CLOUDE_API_KEY')

cwd = os.getcwd()

DEFINITION_DIR = 'data_definition'

os.makedirs(
    os.path.join(
        cwd,
        DEFINITION_DIR
    ),
    exist_ok=True
)

ERROR_MESSAGE = 'We are facing an issue at this moment, please try after sometime.'
