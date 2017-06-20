from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
import time 
from sample_application.UPC import UPC_Wolmart
from pymongo import MongoClient
#Specify mongodb host and datababse to connect to
BROKER_URL = 'mongodb://localhost:27017/jobs'
celery = Celery('EOD_TASKS',broker=BROKER_URL)
#Loads settings for Backend to store results of jobs 
celery.config_from_object('settings')

@celery.task
def add():
	Wolmart=UPC_Wolmart('http://api.walmartlabs.com/v1/items','3ayec4g84mbybsmhr3des5t6')
	client = MongoClient('mongodb://localhost:27017/')
	db=client['sample_application']
	Wolmart.update(db)
