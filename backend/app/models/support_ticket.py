from app.extension import db
from datetime import datetime



class SupportTicket(db.Model):

    __tablename__ = "support_tickets"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id"
        ),
        nullable=False
    )


    subject = db.Column(
        db.String(200)
    )


    status = db.Column(
        db.String(30),
        default="open"
    )


    priority = db.Column(
        db.String(30),
        default="medium"
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


    messages = db.relationship(
        "SupportMessage",
        backref="ticket",
        lazy=True
    )