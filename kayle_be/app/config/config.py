# HOST = '10.101.1.51'
# PORT = '3306'
# DATABASE = 'qa_tools'
# USERNAME = 'root'
# PASSWORD = '123456'

# 本地 mysql
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'qa_tools'
USERNAME = 'root'
PASSWORD = '0819shenxh'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SECRET_KEY = "abc"

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'