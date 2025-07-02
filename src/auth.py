from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.constants.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
import validators
from src.database import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__,url_prefix='/api/v1/auth')

@auth.post('/register')
def register():
   username = request.json['username']
   email = request.json['email']
   password = request.json['password']

   if len(password) < 6:
      return jsonify({'error': "Password length should be more than 6"}), HTTP_400_BAD_REQUEST
   
   if len(username) <= 3:
      return jsonify({'error': "username should be 3 or more characters"}), HTTP_400_BAD_REQUEST
   
   if User.query.filter_by(username=username).first() is not None:
      return jsonify({'error': "username is already taken"}), HTTP_409_CONFLICT
   
   if not username.isalnum() or " " in username:
      return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

   if not validators.email(email):
      return jsonify({'error': "invalid email address"}), HTTP_400_BAD_REQUEST
   
   if User.query.filter_by(email=email).first() is not None:
      return jsonify({'error': "email already taken"}), HTTP_409_CONFLICT
   
   pwd_hash=generate_password_hash(password=password)

   user=User(username=username, email=email, password=pwd_hash)
   db.session.add(user)
   db.session.commit()

   return jsonify({
      'message': 'user created',
      "user": user.serialize()
   }), HTTP_201_CREATED

@auth.post('/login')
def login():
   email = request.json.get('email', '')
   password = request.json.get('password', '')

   user = User.query.filter_by(email=email).first()

   if user:
      is_pass_correct = check_password_hash(user.password, password)

      if is_pass_correct:
         refresh_token = create_refresh_token(identity=str(user.id))
         access_token = create_access_token(identity=str(user.id))

         return jsonify({
            "user": {
               "access_token": access_token,
               'refresh_token': refresh_token,
               "username": user.username,
               "email": user.username
            }
         }), HTTP_200_OK
      else:
         return jsonify({
            "error": "Wrong credentials"
         }), HTTP_401_UNAUTHORIZED  

   
@auth.get('/me')
@jwt_required()
def me():
   user_id = get_jwt_identity()

   user = User.query.filter_by(id=user_id).first()

   return jsonify({
      "user": user.serialize()
   }), HTTP_200_OK


@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
   identity = get_jwt_identity()
   access=create_access_token(identity=identity)

   return jsonify({
      "access_token": access
   }), HTTP_200_OK