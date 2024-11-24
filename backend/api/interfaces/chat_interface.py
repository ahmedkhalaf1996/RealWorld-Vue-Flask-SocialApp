from flask_restx import fields, Namespace

chat_ns = Namespace('chat', description='Chat Releated opreations')

message_model = chat_ns.model('Message',{
    'content': fields.String(required=True, description='the content of the message'),
    'sender': fields.String(required=True, description='the id of the message sender'),
    'recever': fields.String(required=True, description='the id of the message recever'),
})

chatquery_from_fsuid = chat_ns.parser()
chatquery_from_fsuid.add_argument('from', type=int, help='starting pooint for fetiching message ', location='args')
chatquery_from_fsuid.add_argument('firstuid', type=str, required=True, help='First User Id', location='args')
chatquery_from_fsuid.add_argument('seconduid', type=str, required=True, help='Second User Id', location='args')

chatQuery_uid = chat_ns.parser()
chatQuery_uid.add_argument('userid', type=str,help='User Id For unreaded messages ', location='args')


chatqery_main_other = chat_ns.parser()
chatqery_main_other.add_argument('mainuid', type=str, required=True, help='Main User Id', location='args')
chatqery_main_other.add_argument('otheruid', type=str, required=True, help='Other User Id', location='args')