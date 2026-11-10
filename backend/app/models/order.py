from app.extension import db
from datetime import datetime



class Order(db.Model):

    __tablename__ = "orders"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    order_number = db.Column(
        db.String(50),
        unique=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id"
        ),
        nullable=False
    )


    status = db.Column(
        db.String(30),
        default="pending"
    )


    total_amount = db.Column(
        db.Float,
        default=0
    )


    delivery_address = db.Column(
        db.Text
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    items = db.relationship(
        "OrderItem",
        backref="order",
        lazy=True
    )