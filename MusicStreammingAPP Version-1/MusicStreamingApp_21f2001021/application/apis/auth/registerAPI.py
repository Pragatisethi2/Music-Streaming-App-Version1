# import essential libaries
from flask import jsonify
import secrets
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash
from flask_restful import Resource, reqparse

# import table
from application.data.models import db, User

 
user_post_args = reqparse.RequestParser()
user_post_args.add_argument('name', type=str, required=True, help="Name is required !!")
user_post_args.add_argument('email_id', type=str, required=True, help="Username is required !!")
user_post_args.add_argument('password', type=str, required=True, help='password is required')


# register use api
class RegisterAPI(Resource):
    def post(self):
        args = user_post_args.parse_args()
        name= args.get('name')
        email_id = args.get('email_id')
        password = args.get('password')

        user = User.query.filter_by(email_id= email_id).first()
        # if user already register throw status failed
        if user:
            return jsonify({'status':'failed','message': 'Mail is already registered !!'})
        
        hash_password = generate_password_hash(password)

        new_user = User(name=name,password=hash_password,email_id=email_id)  
        new_user.fs_uniquifier = secrets.token_hex(16)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'status' : 'success', 'message': 'Successfully Registered !!'})
    

# {
#     "name" : "user2"
#     "email_id" : "user2@gamil.com",
#     "password" : "1234"
# }