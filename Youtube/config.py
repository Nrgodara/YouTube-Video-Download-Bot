import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7284388982:AAGrfpwjJNdOiUtr1W4JZexazFbJ-_ADEUw")
    API_ID = int(os.environ.get("API_ID", 29337172))
    API_HASH = os.environ.get("API_HASH", "34b3a05a2038e77119115c6ee1ec9d56")
    CHANNEL = os.environ.get("CHANNEL", "-1002059087867")
    HTTP_PROXY = ''
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://t25821653:sUUQp5IhqoRDlwEj@cluster0.jrwf82r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DB_NAME = os.environ.get("DB_NAME", "mydatabase")  # Add your database name here
    ADMIN_IDS = [1280494242, 6703267231]  # Add your admin user IDs here
