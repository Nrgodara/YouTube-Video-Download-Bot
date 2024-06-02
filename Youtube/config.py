import os

class Config(object):
     
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7284388982:AAGrfpwjJNdOiUtr1W4JZexazFbJ-_ADEUw")
    API_ID = int(os.environ.get("API_ID",29337172 ))
    API_HASH = os.environ.get("API_HASH", "34b3a05a2038e77119115c6ee1ec9d56")
    #Add your channel id. For force Subscribe.
    CHANNEL = os.environ.get("CHANNEL", "-1002059087867")
    #Skip or add your proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = ''
