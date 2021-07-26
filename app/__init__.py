import os
from app import config
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import logging 

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()
fileHandler = logging.FileHandler("{0}/{1}.log".format('log', 'app'))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
logger.setLevel(logging.DEBUG)

engine = sqlalchemy.create_engine('mssql+pyodbc://'+ 
                     os.environ["DB_SERVER"] + '/' + 
                     os.environ["DB_NAME"] + '?driver=' + 
                     os.environ["DB_DRIVER"])
connection = engine.connect()
session = sessionmaker(engine)    

# import pyodbc 
# conn = pyodbc.connect('Driver={SQL Server};'
#                      'Server=LAPTOP-QDH3PMIF;'
#                      'Database=master;'
#                      'Trusted_Connection=yes;')
# cursor = conn.cursor()
