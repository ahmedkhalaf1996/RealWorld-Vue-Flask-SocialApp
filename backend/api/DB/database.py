import pymongo

class DataBase():
    def connect():
        try:
          mongo = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS = 1000
          )
        except:
            print("Error - Cannont connect to db")
        return mongo.social