from flask_restx import fields, Namespace

user_ns = Namespace('user', description="user related operations")

user_signup = user_ns.model('Signup', {
    'firstName': fields.String(required=True, description='The user first name'),
    'lastName': fields.String(required=True, description='The user last name'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password')
})


user_signin = user_ns.model('Signin', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password')
})

user_update = user_ns.model('Update', {
    'name': fields.String(required=True, description='The user name'),
    'bio': fields.String(required=True, description='The user bio'),
    'imageUrl': fields.String(required=True, description='The user imageUrl')
})


query_parser_id = user_ns.parser()
query_parser_id.add_argument('id', type=str, required=True, help='User ID', location='args')