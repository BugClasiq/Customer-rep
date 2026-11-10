from flask import Blueprint, request, jsonify
from app.models.user import User
import bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password", "").encode()

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password, user.password.encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role
    })



@auth_bp.route("/signup", methods=["POST"])
def sign_up():
    data = request.get_json() or {}
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    phone_number = data.get("phone_number")
    address = data.get("address")
    password = data.get("password", "").encode()
    confirm_password = data.get("confirm_password", "").encode()

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"error": "User already exists"}), 400


    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role
    })