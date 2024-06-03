from pymongo import MongoClient

client = MongoClient(Config.MONGO_URL)
db = client[Config.DB_NAME]
users_collection = db['users']

def add_user(user_id):
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})

def get_all_users():
    return users_collection.find({})
