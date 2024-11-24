from flask import Flask 
from DB.database import DataBase
from flask_cors import CORS 
from flask_restx import Api
from router.user import user_ns
from router.posts import post_ns
from router.chat import chat_ns
from router.notify import notification_ns
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app, 
          authorizations={
              'BearerAuth':{
                'type': 'apiKey',
                'in': 'header',
                'name':'Authorization'
              }
          },
          varsion="1.0", 
          titile="Socail App API", 
          description="A soical app api", doc='/docs')
    
# connect to mongodb
DataBase.connect()


# register namespaces
api.add_namespace(user_ns)
api.add_namespace(post_ns)
api.add_namespace(chat_ns)
api.add_namespace(notification_ns)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)





