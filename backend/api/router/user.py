import json
from flask import request, Response 
from flask_restx import Namespace, Resource 
from auth.auth_bearer import token_required
from auth.auth_handler import decodeJWT
from services.userService import UserService
from interfaces.user_interface import user_ns, user_signup, user_signin, user_update, query_parser_id


@user_ns.route('/signup')
class UserSignUp(Resource):
    @user_ns.expect(user_signup, validate=True)
    def post(self):
        user = request.get_json()
        try:
            return UserService.createUser(user)
        except Exception as ex:
            return Response(
                response=json.dumps(
                    {"message": "Cannot create User", "error": f"{ex}"}
                ),
                status=500,
                mimetype="application/json"
            )


@user_ns.route('/signin')
class UserSignIn(Resource):
    @user_ns.expect(user_signin, validate=True)
    def post(self):
        user = request.get_json()
        try :
            response = UserService.authenticate(user)
            if response:
                return response
            else:    
                return Response(
                    response=json.dumps(
                        {"error": "Email Or Password is Not Correct"}
                    ),
                    status=401,
                    mimetype="application/json"
                )

        except Exception as ex:
            return Response(
                response=json.dumps(
                    {"error": "Internal Server Error", "deatils": f"{ex}"}
                ),
                status=500,
                mimetype="application/json"
            )


@user_ns.route('/getUser/<id>')
class UserGet(Resource):
    def get(self, id:str):
        data = UserService.getUserByid(id)
        if not data:
            return Response(
                response=json.dumps(
                    {"error": "User not found"}
                ),
                status=404,
                mimetype="application/json"
            )
        return {"user": data["user"], "posts": data['posts']}
    

@user_ns.route('/Update/<id>')
class UserUpdate(Resource):
    @user_ns.expect(user_update, validate=True)
    @user_ns.doc(security="BearerAuth")
    @token_required
    def patch(self, id: str):
        userFromAuth = decodeJWT(request.headers["authorization"].split()[1])["user_id"]
        if userFromAuth != id :

            return Response(
                response=json.dumps(
                    {"error": "you are not authorized to update this user data with provided id."}
                ),
                status=400,
                mimetype="application/json"
            )
        
        userbody = request.get_json()
        try:
            return UserService.UpdateUser(userbody, id)
        except:
            return Response(
                response=json.dumps(
                    {"error": "Can not Update user data."}
                ),
                status=400,
                mimetype="application/json"
            )
           

@user_ns.route('/<id>/following')
class UserFollowing(Resource):
    @token_required
    @user_ns.doc(security="BearerAuth")
    def patch(self, id: str):
        NextUserid = decodeJWT(request.headers["authorization"].split()[1])["user_id"]
        try:
          return UserService.FollowingUser(id, NextUserid)
        except:
            return Response(
                response=json.dumps(
                    {"error": "Can't Follow The User"}
                ),
                status=400,
                mimetype="application/json"
            ) 
        
@user_ns.route('/getSug')
class UserSuggestions(Resource):
    @user_ns.expect(query_parser_id)
    def get(self):
        id = request.args.get("id")
        print("user id", id)
        try: 
            return UserService.GetSugUsers(id)
        except:
            return Response(
                response=json.dumps(
                    {"error": "No Suggestion users"}
                ),
                status=494,
                mimetype="application/json"
            ) 
        

