from app.extension import db
from datetime import datetime


class User(db.Model):

    __tablename__ = "users"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    first_name = db.Column(
        db.String(50),
        nullable=False
    )


    last_name = db.Column(
        db.String(50),
        nullable=False
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )


    password = db.Column(
        db.String(255),
        nullable=False
    )


    phone = db.Column(
        db.String(20)
    )


    address = db.Column(
        db.Text
    )


    role = db.Column(
        db.String(20),
        default="customer"
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # Relationships

    orders = db.relationship(
        "Order",
        backref="customer",
        lazy=True
    )


    tickets = db.relationship(
        "SupportTicket",
        backref="customer",
        lazy=True
    )