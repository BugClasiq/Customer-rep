from app.extension import db
from datetime import datetime



class Product(db.Model):

    __tablename__ = "products"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    name = db.Column(
        db.String(100),
        nullable=False
    )


    category = db.Column(
        db.String(100)
    )


    description = db.Column(
        db.Text
    )


    price = db.Column(
        db.Float,
        nullable=False
    )


    quantity = db.Column(
        db.Integer,
        default=0
    )


    status = db.Column(
        db.String(30),
        default="available"
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