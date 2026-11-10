from app.extension import db



class Setting(db.Model):

    __tablename__ = "settings"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    key = db.Column(
        db.String(100),
        unique=True
    )


    value = db.Column(
        db.Text
    )