from Config import DATABASE_URL
import pymongo


DATABASE = None
def connect_database(Bot_name):
    global DATABASE
    print("connecting to database")
    Bot_name = str(Bot_name).replace('[','').replace(']','')
    if DATABASE_URL != None:
        client = pymongo.MongoClient(DATABASE_URL)
        try:DATABASE = client[(Bot_name)]
        except: DATABASE = client['cluster2']
        print('MongoDB Connected')


def get_database():
    global DATABASE
    return DATABASE

