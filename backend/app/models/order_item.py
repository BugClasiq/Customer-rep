from app.extension import db



class OrderItem(db.Model):

    __tablename__ = "order_items"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    order_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "orders.id"
        ),
        nullable=False
    )


    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "products.id"
        ),
        nullable=False
    )


    quantity = db.Column(
        db.Integer,
        default=1
    )


    price = db.Column(
        db.Float
    )


    product = db.relationship(
        "Product"
    )