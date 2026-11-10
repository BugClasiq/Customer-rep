from app.extension import db
from datetime import datetime



class SupportMessage(db.Model):

    __tablename__ = "support_messages"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    ticket_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "support_tickets.id"
        ),
        nullable=False
    )


    sender = db.Column(
        db.String(20)
    )


    message = db.Column(
        db.Text,
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )