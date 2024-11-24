from functools import wraps
import json
from bson import ObjectId
import jwt 
from flask import Response, request, abort

# db connection & get schema
from DB.database import DataBase

DB = DataBase.connect()
userSchema = DB.users 

# end db connection

JWT_SECRET = "BfFd7XxkMHVo5M59JB7K2kzwP4JoGeeMHqh93uznTRQ="
JWT_ALGORIITHM = "HS256"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # chekc if the authorization headfer is present 
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                return Response(
                    response=json.dumps({
                        "message": "Bearer token malformed",
                        "data": None,
                        "error": "Unauthorized"
                    }),
                    status=401,
                    mimetype='application/json'
                )
            
        else:
            return Response(
                response=json.dumps({
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }),
                status=401,
                mimetype='application/json'
            )
        
        try:
            data= jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORIITHM])
            current_user = userSchema.find_one({"_id": ObjectId(data["user_id"])})
            if current_user is None:
              return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "unauthorized"
              }, 500
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated




