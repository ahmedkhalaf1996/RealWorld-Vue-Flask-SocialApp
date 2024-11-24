import json
from bson import ObjectId
from flask import Response
import pymongo


#  db connetion get schema
from DB.database import DataBase
DB = DataBase.connect()
notificationSchema  = DB.notifications
# end of db Connection

class NotificationService:
    @staticmethod
    def getuserNofication(userid):
        try:
            filter = {"mainuid": {"$regex": userid, "$options": "i"}}
            notifications = list(notificationSchema.find(filter).sort("_id", -1))
            for n in notifications:
                n["_id"] = str(n["_id"])
                n["createdAt"] = str(n["createdAt"])

            return Response(
                response=json.dumps({"notifications": notifications}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            print("error get user notifications: ", e)
            return Response(
                response=json.dumps({"notifications": []}),
                status=500,
                mimetype="application/json"
            )

    @staticmethod
    def MarkNotAsReaded(userid):
        try :
            filter = {"mainuid": userid}
            update = {"$set": {"isreded": True}}

            result = notificationSchema.update_many(filter, update)
            print(f"Modified Count: {result.modified_count}" )

            notifications = list(notificationSchema.find(filter).sort("_id", pymongo.DESCENDING))

            for n in notifications:
                n["_id"] = str(n["_id"])
                n["createdAt"] = str(n["createdAt"])

            notifications.reverse()


            return Response(
                response=json.dumps({"notifications": notifications}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            print("error marking notifications as readed: ", e)
            return Response(
                response=json.dumps({"notifications": []}),
                status=500,
                mimetype="application/json"
            )



