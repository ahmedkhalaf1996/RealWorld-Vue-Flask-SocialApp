from flask_restx import fields, Namespace

post_ns = Namespace('posts', description='Post Releated opreations')

post_create = post_ns.model('CreatePost',{
    'title': fields.String(required=True, description='The post title'),
    'message': fields.String(required=True, description='The post message'),
    'selectedFile': fields.String(required=True, description='The post selectedFile'),
})

post_update = post_ns.model('UpdatePost',{
    'title': fields.String(required=True, description='The post title'),
    'message': fields.String(required=True, description='The post message'),
    'selectedFile': fields.String(required=True, description='The post selectedFile'),
})


post_comment = post_ns.model('CommentPost',{
    'value': fields.String(required=True, description='The post value')
})


post_q_search = post_ns.parser()
post_q_search.add_argument('searchQuery', type=str, required=True, help='Search query', location='args')


post_q_parser = post_ns.parser()

post_q_parser.add_argument('page', type=str,help='page query', location='args')
post_q_parser.add_argument('id', type=str, required=True, help='id query', location='args')



