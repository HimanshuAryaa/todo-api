from flask import request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from extensions import db, bcrypt

auth = Blueprint("auth", __name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)


@auth.route("/register", methods=["POST"])
def register():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()
    if user:
        return jsonify({"Error": "Email Already Exist"}), 400

    hs_password = bcrypt.generate_password_hash(data["password"])

    user_add = User(email= data["email"], password= hs_password)
    db.session.add(user_add)
    db.session.commit()
    return jsonify({"message": "User Registered Successfully"}), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"Error": "User not found"}), 401
    if bcrypt.check_password_hash(user.password, data["password"]):
        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token}), 200
    else:
        return jsonify({"Error": "Wrong Password"}), 401
        
