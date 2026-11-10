from flask import Blueprint, request, jsonify
from app.extension import db
from app.models.user import User
import bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


def _user_payload(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role
    }


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify(_user_payload(user)), 200


@auth_bp.route("/signup", methods=["POST"])
def sign_up():
    data = request.get_json(silent=True) or {}
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    phone_number = (data.get("phone_number") or "").strip() or None
    address = (data.get("address") or "").strip() or None
    password = data.get("password") or ""
    confirm_password = data.get("confirm_password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    if not first_name or not last_name:
        return jsonify({"error": "First name and last name are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        phone=phone_number,
        address=address,
        role="customer",
    )
    db.session.add(user)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not create account"}), 500

    return jsonify(_user_payload(user)), 201
