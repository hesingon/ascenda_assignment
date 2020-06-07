from pymongo import MongoClient
from configs.sources import MONGO_HOST, MONGO_PORT

client = MongoClient(MONGO_HOST, MONGO_PORT)
