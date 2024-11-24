import json 
from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource

from auth.auth_bearer import token_required
from auth.auth_handler import decodeJWT
from services.postService import PostService

from interfaces.post_interface import post_create, post_update, post_comment, post_q_search, post_q_parser, post_ns

post_router = Blueprint('posts', __name__)

@post_ns.route("")
class PostList(Resource):
    @post_ns.expect(post_create, validate=True)
    @token_required
    @post_ns.doc(security='BearerAuth')
    def post(self):
        try :
          pData = request.get_json()
          Userid = decodeJWT(request.headers["authorization"].split()[1])["user_id"]
          pData['creator'] = Userid
          return PostService.createPost(pData)
        except:
            return Response(
                response=json.dumps({"message": "something went wrong!"}),
                status=500,
                mimetype="application/json"
            )


    @post_ns.expect(post_q_parser)
    def get(self):
        try:
          args = post_q_parser.parse_args()
          page = args.get("page")
          id = args.get("id")
          return PostService.GetAllPosts(page, id)
        except:
            return Response(
                response=json.dumps({"message": "No Posts"}),
                status=500,
                mimetype="application/json"
            )
  
@post_ns.route("/<id>")
class Post(Resource):
   def get(self, id):
    post = PostService.GetPostById(id)
    if not post:
       return Response(
                response=json.dumps({"message": "post not found"}),
                status=404,
                mimetype="application/json"
            )     
    return post 
# update post 
   @token_required
   @post_ns.doc(security='BearerAuth')
   @post_ns.expect(post_update, validate=True)
   def patch(self, id ):
      try:
        Userid = decodeJWT(request.headers["authorization"].split()[1])["user_id"]
        post = PostService.GetPostById(id)
        if not post:
         return Response(
                    response=json.dumps({"message": "post not found"}),
                    status=404,
                    mimetype="application/json"
                ) 
        if post['post']['creator']  != Userid:
         return Response(
                    response=json.dumps({"error": "you are not authorized to update this post"}),
                    status=500,
                    mimetype="application/json"
                ) 

        body = request.get_json()
        return PostService.UpdatePost(id, body)
      except:  
         return Response(
                    response=json.dumps({"message": "can not update post"}),
                    status=500,
                    mimetype="application/json"
                ) 
   

# delete post 
   @token_required
   @post_ns.doc(security='BearerAuth')
   def delete(self, id):
      try:
        Userid = decodeJWT(request.headers["authorization"].split()[1])["user_id"]
        post = PostService.GetPostById(id)
        if not post:
         return Response(
                    response=json.dumps({"message": "post not found"}),
                    status=404,
                    mimetype="application/json"
                ) 
        if post['post']['creator']  != Userid:
         return Response(
                    response=json.dumps({"error": "you are not authorized to delete this post"}),
                    status=500,
                    mimetype="application/json"
                ) 
        #   authorized to delete        
        return PostService.DeletePost(id)
      except:
            return Response(
            response=json.dumps({"message": "can not delete post"}),
            status=500,
            mimetype="application/json"
        )  


@post_ns.route("/<id>/commentPost")
class PostComment(Resource):
   @token_required
   @post_ns.doc(security='BearerAuth')
   @post_ns.expect(post_comment, validate=True)
   def post(self, id):
      try:
        data = request.get_json()
        useridCom = decodeJWT(request.headers["authorization"].split()[1])["user_id"]
        return PostService.CommentPostMethod(data, id, useridCom)
      except Exception as e:
        print("ex", e)
        return Response(
            response=json.dumps({"message": "unable to add your commnet!"}),
            status=500,
            mimetype="application/json"
        )  
      
@post_ns.route("/search")
class PostSearch(Resource):
   @post_ns.expect(post_q_search)
   def get(self):
      try:
         search = request.args.get("searchQuery")
         return PostService.GetPostUsersBySearch(search)
      except:
        return Response(
            response=json.dumps({"Error": "No User Or Posts Result"}),
            status=400,
            mimetype="application/json"
        )  
      
@post_ns.route("/<id>/likePost")
class PostLike(Resource):
   @token_required
   @post_ns.doc(security='BearerAuth')
   def patch(self, id):
      try:
        Userid = decodeJWT(request.headers["authorization"].split()[1])["user_id"]
        return PostService.LikePost(id, Userid)
      except:
         return Response(
            response=json.dumps({"message": "can not like the post"}),
            status=400,
            mimetype="application/json"
        )          