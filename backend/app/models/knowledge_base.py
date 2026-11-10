from app.extension import db
from datetime import datetime



class KnowledgeBase(db.Model):

    __tablename__ = "knowledge_base"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(200),
        nullable=False
    )


    content = db.Column(
        db.Text,
        nullable=False
    )


    type = db.Column(
        db.String(50)
    )


    keywords = db.Column(
        db.String(255)
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