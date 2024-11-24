import math 
import json
from typing import Optional
from bson import ObjectId
from flask import Response
import pymongo
from models.unReadedmessage_model import UnReadedMsg
from models.message_model import Message

# db connection getSchema 
from DB.database import DataBase

DB = DataBase.connect()
userSchema = DB.users
messageSchema = DB.messages
unReadedMsgSchema = DB.unreadedmsg

# ========================


class ChatService:
    @staticmethod
    def sendMessage(msg):
        try:
            msg_in = Message(
                content= str(msg['content']),
                sender= str(msg['sender']),
                recever= str(msg['recever']),
            )

            dbResponse = messageSchema.insert_one(dict(msg_in))
            if dbResponse.inserted_id:
                newMsg = messageSchema.find_one({"_id": ObjectId(dbResponse.inserted_id)})

            # update unreadedMsg 
            sender = str(msg['sender'])
            recever = str(msg['recever'])

            ChatService.update_unreaded_messages(sender, recever)

            newMsg["_id"] = str(newMsg["_id"])
            return Response(
                response=json.dumps(newMsg),
                status=201,
                mimetype="application/json"
            )
        except:
            return None

# helper func 
    @staticmethod
    def update_unreaded_messages(sender, recever):
        try:
            existing_recored = unReadedMsgSchema.find_one_and_update(
                {"mainUserid": recever, "otherUserid": sender},
                {"$inc": {"numOfUnreadedMessages":1}, "$set":{"isReaded": False}},
                upsert=True,
                return_document=pymongo.ReturnDocument.AFTER
            )

            if not existing_recored:
                unReadedMsgSchema.insert_one({
                    "mainUserid": recever,
                    "otherUserid": sender,
                    "numOfUnreadedMessages": 1,
                    "isReaded": False
                })

            print("Update or created unreadedmsg docuent")
        except Exception as e:
            print("Error updateing or creating UnreadedMsg Dcoument:", e)


    # get message by nunmber 
    @staticmethod
    def GetMsgByNums(from_val, firstuid, seconduid):
        try:
            sender_filtter = {"sender": firstuid, "recever": seconduid}
            recever_filtter = {"sender": seconduid, "recever": firstuid}

            messages = list(messageSchema.find({"$or":[sender_filtter, recever_filtter]})
                            .sort("_id", -1).skip(from_val * 8).limit(8))
            for ms in messages:
                ms["_id"] = str(ms["_id"])
            
            messages_lit =list(messages)
            messages_lit.reverse()

            return Response(
                response=json.dumps(
                    {"msgs": messages_lit}
                ),
                status=200,
                mimetype="application/json"
            )
            
        except Exception as e:
            print(e)
            return "Internal Server Error From chat Service", 500


    @staticmethod
    def GetUserUnREdedMsg(userid):
        try:
            urms = list(unReadedMsgSchema.find({"mainUserid": userid, "isReaded": False}))
            total_unreaded_message_count =  sum(msg["numOfUnreadedMessages"] for msg in urms)

            for u in urms:
                u["_id"] = str(u["_id"])

 
            return Response(
                response=json.dumps(
                    {"messages": urms, "total": total_unreaded_message_count}
                ),
                status=200,
                mimetype="application/json"
            )
        except:
            return None
        
    # mark msgs as readed 
    @staticmethod
    def MarkMsgAsReaded(mainuid, otheruid):
        try:
            filter = {"mainUserid": mainuid, "otherUserid": otheruid}
            update = {"$set": {"isReaded": True, "numOfUnreadedMessages": 0}}

            result = unReadedMsgSchema.find_one_and_update(filter, update, upsert=True, return_document=pymongo.ReturnDocument.AFTER)

            if result:
                return Response(
                response=json.dumps(
                    {"isMarked":True}
                ),
                status=200,
                mimetype="application/json"
            ) 
            
            else:
                return Response(
                response=json.dumps(
                    {"isMarked":False}
                ),
                status=200,
                mimetype="application/json"
            )
        except:
            return None