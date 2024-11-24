from flask_restx import fields, Namespace

notification_ns = Namespace('notification', description="Notification realated operations")

query_parser_id = notification_ns.parser()
query_parser_id.add_argument('id', type=str, required=True, help='Nofification user id',location='args' )



