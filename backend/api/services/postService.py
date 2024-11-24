import math 
import json
import re
from typing import Optional
from bson import ObjectId
from flask import Response
import pymongo

from models.posts_model import Post
from models.users_model import User
from models.notification_model import Notification, UserInSchema

#  db connetion get schema
from DB.database import DataBase

DB = DataBase.connect()
userSchema = DB.users 
postSchema = DB.posts 
notificationSchema  = DB.notifications
# end of db Connection


class PostService:
    # create post 
    @staticmethod
    def createPost(post):
        user = userSchema.find_one({"_id": ObjectId(post['creator'])}) 
        post['name'] = str(user['name'])
 
        try:
            post_in = Post(
                title= str(post['title']),
                message= str(post['message']),
                creator= str(post['creator']),
                selectedFile= str(post['selectedFile']),
                name= str(post['name']),
            )

            dbResponse = postSchema.insert_one(dict(post_in))

            if dbResponse.inserted_id:
                result = postSchema.find_one({"_id": ObjectId(dbResponse.inserted_id)})
                result["_id"] = str(result["_id"])
                result["createdAt"] = str(result["createdAt"])
            return Response(
                response=json.dumps(
                    {"result": result}
                ),
                status=201,
                mimetype="application/json"
            )
        except:
            return None
    
    # add comment to the post 
    @staticmethod
    def CommentPostMethod(body, id:str, useridCom:str):
        try:
            post = postSchema.find_one({"_id": ObjectId(id)})
            post['comments'].append(str(body['value']))
            dbResponse = postSchema.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"comments": post['comments']}}
            )
            if dbResponse:
                post = postSchema.find_one({"_id": ObjectId(id)})
                post["_id"] = str(post["_id"])
                post["createdAt"] = str(post["createdAt"])
            # TODO call grpc .for raeltime Notification\
            # craete notification 
            user = userSchema.find_one({"_id": ObjectId(useridCom)})
            notify_in = Notification(
                deatils=f"{user['name']} Commented On Your Post",
                mainuid=post['creator'],
                targetid=id,
                user=UserInSchema(
                    name=user['name'],
                    avatar=user['imageUrl']
                )
            )
            
            notificationSchema.insert_one(notify_in.dict())

            return Response(
                response=json.dumps(
                    {"data": post}
                ),
                status=201,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps(
                    {"error": "faild commmnnet on post ", "e": e}
                ),
                status=500,
                mimetype="application/json"
            )
        

    # getting posts or users or both
    @staticmethod
    def GetPostUsersBySearch(searchQuery: str):
        try: 
          regex = re.compile(re.escape(searchQuery), re.IGNORECASE)
          posts = list(postSchema.find({"$or":[{"title":{"$regex": regex}}, {"message":{"$regex":regex}}]})) 
          users = list(userSchema.find({"name": {"$regex": regex}})) 
          
          for post in posts:
                post["_id"] = str(post["_id"])
                post["createdAt"] = str(post["createdAt"])

          for user in users:
              user["_id"] = str(user["_id"])

          return Response(
                response=json.dumps(
                    {"posts": posts, "user":users}
                ),
                status=200,
                mimetype="application/json"
            )
        except: 
            None

    # GetPostByID
    @staticmethod
    def GetPostById(id:str):
        try:
            post = postSchema.find_one({"_id": ObjectId(id)})
            post["_id"] = str(post["_id"])
            post["createdAt"] = str(post["createdAt"])
            return {"post": post}
        except:
            return None


     # Get5 All posts releted to the user && with Pagenation
    @staticmethod
    def GetAllPosts(pageStr: str , id: str):
        try:
            page = 1
            if pageStr:
                page = int(pageStr)
            
            Limit = 2 
            startIndex = (int(page) -1) * Limit

            MainUser = userSchema.find_one({"_id": ObjectId(id)})
            MainUser['following'].append(str(MainUser['_id']))

            MainStr = []
            for uid in MainUser['following']:
                MainStr.append( {"creator": str (uid)} )
            
            # search 
            total = postSchema.count_documents({"$or": MainStr})

            Posts = list(postSchema.find({"$or": MainStr})
                         .sort([('_id', pymongo.DESCENDING)])
                         .limit(Limit)
                         .skip(startIndex))
            for post in Posts:
                post["_id"] = str(post["_id"])
                post["createdAt"] = str(post["createdAt"])
            
            return {
                "data": Posts,
                "currentPage": page,
                "numberOfPages": math.ceil(float(total) / float(Limit))
            }
        except:
            return None 
        
    # update post 
    @staticmethod
    def UpdatePost(id: str, newPost):
        try:
            updatedpost = {"title":newPost['title'],"message":newPost['message'],"selectedFile":newPost['selectedFile']}
            postSchema.update_one({"_id": ObjectId(id)}, {"$set": updatedpost})

            updated =  postSchema.find_one({"_id": ObjectId(id)})
            updated["_id"] = str(updated["_id"])
            updated["createdAt"] = str(updated["createdAt"])

            return {"data": updated}
        except:
            return None

    # like post 
    @staticmethod
    def LikePost(id:str, UserId:str):
        try:
         post = postSchema.find_one({"_id": ObjectId(id)})
         if UserId in post['likes']:
             post['likes'].remove(UserId)
         else:
            post['likes'].append(UserId)
            # TODO call grpc .for raeltime Notification\
            # craete notification 
            user = userSchema.find_one({"_id": ObjectId(UserId)})
            notify_in = Notification(
                deatils=f"{user['name']} Like Your Post",
                mainuid=post['creator'],
                targetid=id,
                user=UserInSchema(
                    name=user['name'],
                    avatar=user['imageUrl']
                )
            )
            
            notificationSchema.insert_one(notify_in.dict())



         postSchema.update_one({"_id": ObjectId(id)},{"$set": {"likes": post['likes']}})
         post["_id"] = str(post["_id"])
         post["createdAt"] = str(post["createdAt"])
         return {"post": post}
        except Exception as e:
            print("like error", e)
            return None 
        
    # delete post 
    @staticmethod
    def DeletePost(id:str):
        try:
            post = postSchema.delete_one({"_id": ObjectId(id)})
            if post :
                return {"message": "post Deleted Successfully."}
        except:
            return None 
    