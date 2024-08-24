from flask import Blueprint,jsonify,request
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt,jwt_required
from app.database.models import *


auth_bp = Blueprint('auth_bp',__name__)

@auth_bp.post('/testregister')
def register_user():
    data= request.get_json()
    user = Users.get_user_by_email(email=data.get("email"))

    if user is not None:
        return jsonify({"message": "User already exists"}), 409
    else:
        user =Users(
            email=data.get("email"),
            first_name =data.get("first_name"),
            second_name=data.get("second_name"),
            role = data.get("role")
        )
        user.set_password(data.get('password'))
        user.save()
        return jsonify({"message":"User created"}),201
    

@auth_bp.post('/testlogin')
def login_user():

    data= request.get_json()
    user = Users.get_user_by_email(email=data.get('email'))

    if user and (user.check_password(password=data.get('password'))):
        accesstoken= create_access_token(identity=user.email,)
        refreshtoken= create_refresh_token(identity=user.email)
        return jsonify({
            "message":"Logged In",
            "tokens":{
                "access":accesstoken,
                "refresh":refreshtoken
            }
        }),200
    
    return jsonify({"error":"invalid email or password"}),400

@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    token = get_jwt()
    email = token.get("sub")
    return jsonify({"email":email})