from app.extension import db
from datetime import datetime



class AuditLog(db.Model):

    __tablename__ = "audit_logs"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    actor = db.Column(
        db.String(50)
    )


    action = db.Column(
        db.String(100)
    )


    description = db.Column(
        db.Text
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )