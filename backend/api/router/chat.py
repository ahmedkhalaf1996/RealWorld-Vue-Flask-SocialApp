import json 
from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource

from auth.auth_bearer import token_required
from auth.auth_handler import decodeJWT
from services.chatService import ChatService

from interfaces.chat_interface import chat_ns, message_model, chatqery_main_other, chatQuery_uid, chatquery_from_fsuid

chat_router = Blueprint('chat', __name__)

@chat_ns.route('/sendmessage')
class SendMessage(Resource):
    @chat_ns.expect(message_model)
    def post(self):
        try:
            data = request.get_json()
            return ChatService.sendMessage(data)
        except:
            return Response(
                response=json.dumps(
                    {"message": "Unable to send message!"}
                ),
                status=500,
                mimetype="application/json"
            )

@chat_ns.route('/getmsgsbynums')
class GetMsgsByNums(Resource):
    @chat_ns.expect(chatquery_from_fsuid, validate=True)
    def get(self):
        try:
            from_val = int(request.args.get('from', 0))
            firstuid = request.args.get('firstuid')
            seconduid = request.args.get('seconduid')
            
            return  ChatService.GetMsgByNums(from_val, firstuid, seconduid)
        except Exception as e:
            print(e)
            return "Internal Server Error", 500


@chat_ns.route('/get-user-unreadedmsg')
class GetUserUnReadedMsg(Resource):
    @chat_ns.expect(chatQuery_uid, validate=True)
    def get(self):
        try:
         userid = request.args.get('userid')
         if not userid:
            return Response(
                response=json.dumps(
                    {"message": "Proplem with provided query paramters."}
                ),
                status=500,
                mimetype="application/json"
            )
         return ChatService.GetUserUnREdedMsg(userid)
        except Exception as e:
            print(e)
            return Response(
                response=json.dumps(
                    {"message": "Proplem with provided query paramters."}
                ),
                status=400,
                mimetype="application/json"
            )


@chat_ns.route('/mark-msg-asreaded')
class MarkMsgAsREaded(Resource):
    @chat_ns.expect(chatqery_main_other, validate=True)
    def get(self):
        try :
            mainuid = request.args.get('mainuid')
            otheruid = request.args.get('otheruid')
            if not mainuid or not otheruid:
             return Response(
                response=json.dumps(
                    {"message": "Proplem with provided query paramters."}
                ),
                status=500,
                mimetype="application/json"
            )

            return ChatService.MarkMsgAsReaded(mainuid, otheruid)
        except Exception as e:
            print(e)
            return Response(
                response=json.dumps(
                    {"message": "Internal server erorr"}
                ),
                status=500,
                mimetype="application/json"
            )