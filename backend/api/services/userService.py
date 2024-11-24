import json 
from typing import Optional 
from bson import ObjectId 
from flask import Response 
from models.users_model import User
from models.notification_model import Notification, UserInSchema
from auth.auth_handler import signJWT
from passlib.context import CryptContext


# pass context
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# conn to db 
from DB.database import DataBase
DB = DataBase.connect()
userSchema = DB.users 
postSchema = DB.posts 
notificationSchema  = DB.notifications
# end conn to db 


class UserService:
    # register user 
    @staticmethod
    def createUser(user):
        user_in = User(
            name= str(user['firstName'] + " " + user['lastName']),
            email=str(user['email']),
            password=password_context.hash(user['password'])
        )

        dbRespose = userSchema.insert_one(dict(user_in))

        if dbRespose.inserted_id:
            result = userSchema.find_one({"_id": dbRespose.inserted_id})
            result["_id"] = str(result["_id"])
            del result["password"]
            token = signJWT(result["_id"])
        return Response(
            response=json.dumps(
                {"result": result, "token":token}
            ),
            status=201,
            mimetype="application/json"
        )

    #  login user 
    @staticmethod
    def authenticate(userBody): 
        user = UserService.get_user_by_email(email=userBody['email'])
        if not user:
            return None 
        if not password_context.verify(userBody['password'], str(user["password"])):
            return None 
        
        token = signJWT(str(user["_id"]))
        user["_id"] = str(user["_id"])
        del user["password"]
        return {"result":user, "token": token['access_token']}
    
    # get user by email
    @staticmethod
    def get_user_by_email(email: str)-> Optional[User]:
        return userSchema.find_one({"email": email})
    
    # Get user by id
    @staticmethod
    def getUserByid(userid:str):
        try:
            user = userSchema.find_one({"_id": ObjectId(userid)})
            user["_id"] = str(user["_id"])

            posts = list(postSchema.find({"creator":userid}))
            if posts:
                for post in posts:
                    post["_id"] = str(post["_id"])
            return {"user":user, "posts":posts}
        except:
            return None
        
    # update user 
    @staticmethod
    def UpdateUser(body, id:str):
        try:
          userbody = {"name":body['name'], "bio":body['bio'], "imageUrl":body['imageUrl']}
          dbResponse = userSchema.update_one(
              {"_id": ObjectId(id)},
              {"$set": userbody}
          )

          if dbResponse:
              user = userSchema.find_one({"_id": ObjectId(id)})
              user["_id"] = str(user["_id"])

              posts = list(postSchema.find({"creator":id}))
              if posts:
                    for post in posts:
                        post["_id"] = str(post["_id"])
              else:
                  posts = []

          return Response(
              response=json.dumps(
                  {"user":user, "posts":posts}
              ),
              status=200,
              mimetype="application/json"
          )
        except:
            return None



    @staticmethod
    def FollowingUser(id:str, NextUserId:str):
        try:
            user1 = userSchema.find_one({"_id": ObjectId(id)})
            user2 = userSchema.find_one({"_id": ObjectId(NextUserId)})
            # check if is nextuser aleady in our main user follwoers list 
            if str(NextUserId) in user1['followers']:
                user1['followers'].remove(str(NextUserId))
                user2['following'].remove(str(id))
            else:
                user1['followers'].append(str(NextUserId))
                user2['following'].append(str(id))
            
            # user user1 and user 2 
            userSchema.update_one({"_id": ObjectId(id)},
                {"$set": {"followers":user1['followers'] , "following":user1['following']}})

            userSchema.update_one({"_id": ObjectId(NextUserId)},
                {"$set": {"followers":user2['followers'] , "following":user2['following']}})
            
            user1["_id"] = str(user1["_id"])
            user2["_id"] = str(user2["_id"])

            #  Start Creating Notification 
            usernotify = userSchema.find_one({"_id": ObjectId(user2["_id"])})
            notify_in = Notification(
                deatils=f"{usernotify['name']} Start Following you.",
                mainuid=user1["_id"],
                targetid=user2["_id"],
                user=UserInSchema(
                    name=usernotify['name'],
                    avatar=usernotify['imageUrl']
                )
            )
            
            notificationSchema.insert_one(notify_in.dict())
            # end crating Notification
            # TODO call grpc 

            return Response(
              response=json.dumps(
                  {"updateduser1":user1, "updateduser2":user2}
              ),
              status=200,
              mimetype="application/json"
          )
        except Exception as ex:
            return Response(
                response=json.dumps(
                    {"message": "Cannont Follwing Or unFollowing The user", "error": f"{ex}"}
                ),
                status=500,
                mimetype="application/json"
            )
        
    # get some suggested users for our user /
    @staticmethod
    def GetSugUsers(id:str):
        try:
            AllSugUsers = []
            MainUser = userSchema.find_one({"_id": ObjectId(id)})

            if MainUser:
                for foides in MainUser['following']:
                    fuser =  userSchema.find_one({"_id": ObjectId(foides)})
                    for i in fuser['followers']:
                      if not str(i) == str(MainUser["_id"]):
                        lastf =  userSchema.find_one({"_id": ObjectId(i)})
                        AllSugUsers.append(lastf)
                    for uid in fuser['following']:
                     if not str(uid) == str(MainUser["_id"]):
                        lastg =  userSchema.find_one({"_id": ObjectId(uid)})
                        AllSugUsers.append(lastg)      

            for user in AllSugUsers:
                user["_id"] = str(user["_id"])

            return {"users": AllSugUsers}
        except:
            return None     


