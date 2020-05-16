import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def get_mambu_user():
    return os.getenv('MAMBU_USER')

def get_mambu_pw():
    return os.getenv('MAMBU_PW')

def get_api_str():
    return os.getenv('API_STR')

def get_secret_key():
    return os.getenv('SECRET_KEY')

def get_jwt_secret_key():
    return os.getenv('JWT_SECRET_STRING')

def get_database_uri():
    user = os.getenv('RDS_USERNAME')
    pw = os.getenv('RDS_PASSWORD')
    url = os.getenv('RDS_URL')
    db = os.getenv('RDS_DB_NAME')
    db_uri = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=user,pw=pw,url=url,db=db)
    return db_uri