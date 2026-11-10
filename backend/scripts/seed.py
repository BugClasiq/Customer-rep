import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extension import db

from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.knowledge_base import KnowledgeBase

import bcrypt



app = create_app()


with app.app_context():


    # Clear old data

    db.drop_all()

    db.create_all()



    # =========================
    # CREATE USERS
    # =========================


    admin_password = bcrypt.hashpw(
        "admin123".encode(),
        bcrypt.gensalt()
    )


    customer_password = bcrypt.hashpw(
        "customer123".encode(),
        bcrypt.gensalt()
    )



    admin = User(

        first_name="Admin",

        last_name="User",

        email="admin@supermarket.com",

        password=admin_password.decode(),

        role="admin"

    )



    customer = User(

        first_name="John",

        last_name="Doe",

        email="john@gmail.com",

        password=customer_password.decode(),

        phone="08012345678",

        address="Lagos Nigeria",

        role="customer"

    )


    db.session.add(admin)

    db.session.add(customer)

    db.session.commit()



    # =========================
    # CREATE PRODUCTS
    # =========================


    products = [

        Product(
            name="Coca Cola 50cl",
            category="Drink",
            description="Cold soft drink",
            price=500,
            quantity=100
        ),


        Product(
            name="Peak Milk",
            category="Dairy",
            description="Full cream milk",
            price=1200,
            quantity=50
        ),


        Product(
            name="Golden Penny Spaghetti",
            category="Food",
            description="500g spaghetti",
            price=800,
            quantity=70
        ),


        Product(
            name="Rice 5kg",
            category="Food",
            description="Premium rice",
            price=7500,
            quantity=30
        ),


        Product(
            name="Bread",
            category="Bakery",
            description="Fresh bread",
            price=700,
            quantity=40
        )

    ]


    db.session.add_all(products)

    db.session.commit()



    # =========================
    # CREATE ORDER
    # =========================


    order = Order(

        order_number="ORD1001",

        user_id=customer.id,

        status="processing",

        total_amount=8700,

        delivery_address="Lagos Nigeria"

    )


    db.session.add(order)

    db.session.commit()



    item1 = OrderItem(

        order_id=order.id,

        product_id=products[1].id,

        quantity=1,

        price=1200

    )


    item2 = OrderItem(

        order_id=order.id,

        product_id=products[3].id,

        quantity=1,

        price=7500

    )


    db.session.add(item1)

    db.session.add(item2)


    db.session.commit()



    # =========================
    # KNOWLEDGE BASE
    # =========================


    policies = [

        KnowledgeBase(

            title="Delivery Policy",

            type="Delivery Policy",

            keywords="delivery time shipping",

            content="""

            Orders are delivered within 24-48 hours.

            Customers receive updates when orders are shipped.

            """

        ),



        KnowledgeBase(

            title="Refund Policy",

            type="Refund Policy",

            keywords="refund money return",

            content="""

            Refund requests must be submitted within 7 days.

            Products must be unused.

            """

        ),



        KnowledgeBase(

            title="Store Opening Hours",

            type="FAQ",

            keywords="opening hours time",

            content="""

            The supermarket opens from 8AM to 8PM every day.

            """

        )

    ]


    db.session.add_all(policies)

    db.session.commit()



    print("Database seeded successfully")