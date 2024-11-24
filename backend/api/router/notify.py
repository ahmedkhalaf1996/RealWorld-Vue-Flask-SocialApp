import json 
from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource

from services.notifyService import NotificationService
from interfaces.notify_interface import notification_ns , query_parser_id

notification_router = Blueprint('notification', __name__)

@notification_ns.route('/mark-notification-asreaded')
class MarkNofificationAsRead(Resource):
    @notification_ns.expect(query_parser_id, validate=True)
    def get(self):
        try:
            id = request.args.get("id")
            return NotificationService.MarkNotAsReaded(id)
        except Exception as e:
            print("er", e)
            return Response(
                response=json.dumps(
                    {"message": "internal Server errro"},
                ),
                status=500,
                mimetype="application/json"
            )
        
@notification_ns.route('/<userid>')
class UserNotifications(Resource):
    def get(self, userid:str):
        try:
            return NotificationService.getuserNofication(userid)
        
        except Exception as e:
            print("er", e)
            return Response(
                response=json.dumps(
                    {"message": "internal Server errro"},
                ),
                status=500,
                mimetype="application/json"
            )




