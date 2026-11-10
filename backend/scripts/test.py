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

    print("Register!!!")

    first_name = input("What is your first name?")
    last_name = input("What is your last name?")
    email = input("What is your email address?")
    password = input("What is your password?")
    phone = input("What is your phone number?")
    address = input("What is your address?")

    customer_password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )


    customer = User(
    
            first_name=first_name,
    
            last_name=last_name,
    
            email=email,
    
            password=customer_password.decode(),
    
            phone=phone,
    
            address=address,
    
            role="customer"
    
        )

    db.session.add(customer)
    
    db.session.commit()

    print("Registration Successful.")


    print("These are our available products!")


    products = Product.query.all()
    for i in products:
        print(i.id, i.name, i.price)

    flag = True
    order_list = []
    total_price = 0

    last_order = Order.query.count()
    new_order = f"ORD{last_order + 1001}"


    make_order = input("do you want to make your first order? (y/n)").lower().strip()

    if make_order == "y":

        order = Order(
        
                order_number=new_order,
        
                user_id=customer.id,
        
                status="processing",
        
                total_amount=total_price,
        
                delivery_address=address
        
            )
        db.session.add(order)
        db.session.commit()
    else:
        flag = False
    


    while flag:
        try:
            order_item = int(input("What item do you want to add to your order? [1-5] (0 to confirm.)"))
        except ValueError:
            print("Please enter a number.")
            continue

        if order_item > 0 and order_item <= len(products):
            order_list.append(order_item)
            order_price = products[order_item-1].price
            
            item = OrderItem(
    
                order_id=order.id,
        
                product_id=order_item,
        
                quantity=1,
        
                price=order_price
        
            )

            total_price += order_price
            db.session.add(item)

        else:
            flag = False


    print(f"This is your order number {new_order} with a price of {total_price}")
    order.total_amount = total_price
    db.session.add(order)
    db.session.commit()


    

    


    
    