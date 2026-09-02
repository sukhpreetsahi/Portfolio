from flask import Flask, render_template, Response, url_for, request, redirect, flash, session, jsonify #Required for frontend communication
from models import db, Users, Products, Orders, Order_items  # Import models
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import re
import os
from dotenv import load_dotenv
load_dotenv()
from flask_wtf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")  # For sessions based security and token security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #link database to app
db.init_app(app)
csrf = CSRFProtect(app)


@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net https://stackpath.bootstrapcdn.com 'unsafe-inline'; "
        "style-src 'self' https://fonts.googleapis.com https://cdn.jsdelivr.net 'unsafe-inline'; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'self';"
    )
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.errorhandler(400)
def handle_csrf_error(e):
    return "CSRF validation failed. Please refresh the page and try again.", 400

with app.app_context():   #If database tables not created, create
    db.create_all()

class Cart:
    def __init__(self):
        self.__items = []  # List to store items in the cart
        self.__total = 0

    def add_item(self, product_id, product_name, quantity, price):
        for item in self.__items:
            if item['product_id'] == product_id:  # Check if the product already exists in the cart
                item['quantity'] += quantity
                item['subtotal'] = item['quantity'] * item['price']
                self.calculate_total()
                return

        # If the product doesn't exist, add it as a new item
        self.__items.append({
            'product_id': product_id,
            'product_name': product_name,
            'quantity': quantity,
            'price': price,
            'subtotal': quantity * price
        })
        self.calculate_total()

    def clear(self):
        self.__items = []  # Clear all items from the cart
        self.__total = 0
    
    def remove_item(self, product_id):
        """Remove an item from the cart by product_id"""
        self.__items = [item for item in self.__items if item['product_id'] != product_id]
        self.calculate_total()

    def calculate_total(self):
        """ Calculate total cost of all products in cart """
        self.__total = 0
        for item in self.__items:
            self.__total += item['subtotal']

    def get_item_quantity(self, product_id):
        """ Returns the current quantity of a specific product in the cart. """
        for item in self.__items:
            if item['product_id'] == product_id:
                return item['quantity']
        return 0  # If the product is not in the cart, return 0
    
    def to_dict(self):
        return {'items': self.__items, 'total': self.__total}

    def get_items(self):
        """ Getter method for private items attribute"""
        return self.__items
    
    def set_items(self, values):
        """ Setter method for private items attribute"""
        self.__items = values

    def get_total(self):
        return self.__total
    
    def set_total(self, value):
        self.__total = value

def get_cart():
    """Get the cart data from the session if there was one"""
    cart_data = session.get('cart', {'items': [], 'total': 0})  # Default total to 0    
    cart = Cart()
    cart.set_items(cart_data['items'])
    cart.set_total(cart_data['total'])
    return cart

def save_cart(cart):
    """Save cart data to the session"""
    session['cart'] = cart.to_dict()

def empty_cart(cart):
    """Clear cart data from session and cart object"""
    cart.clear()
    session['cart'] = cart.to_dict()

def get_product_name(self, product_id):
        """ Return the name of a product from its product id"""
        product = Products.query.get(product_id)
        return product.name

def is_valid_name(name):
    return bool(re.match(r'^[A-Za-z]+$', name))  # Only allows letters, no spaces or symbols

# Validation function for email uniqueness
def is_email_unique(email):
    """ Check if email already in database."""
    return Users.query.filter_by(email=email).first() is None

def is_valid_email(email):
    """ Check if the entered email matches the format of an email address."""
    # Regex pattern for a valid email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_valid_password(password):
    """ Validate password against password policy"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(char in "!@#$%^&*()-_+=<>?/|\\{}[]:;" for char in password):
        return False, "Password must contain at least one special symbol (!@#$%^&*()-_+=<>?/|\\{}[]:;)."
    return True, None

def get_orders_summary(user_id):
    """ Return order data by joining different tables of the database"""
    # Query the data
    results = db.session.query(
        Orders.id,
        Products.productname,
        Order_items.quantity,
        Order_items.subtotal,
        Orders.total_amount
    ).join(Order_items, Orders.id == Order_items.order_id) \
     .join(Products, Order_items.product_id == Products.id) \
     .filter(Orders.customer_id == user_id) \
     .order_by(Orders.id).all()

    # Process the results into a structured format
    orders = {}
    grand_total = 0

    for row in results:
        order_id = row.id
        product_name = row.productname
        quantity = row.quantity
        subtotal = f'{row.subtotal:.2f}'
        total_amount = f'{row.total_amount:.2f}'

        # If the order is not already in the dictionary, initialize it
        if order_id not in orders:
            orders[order_id] = {
                'order_number': order_id,
                'order_items': [],
                'total': total_amount
            }
            grand_total += float(total_amount)

        # Append the product details to the order
        orders[order_id]['order_items'].append({
            'product_name': product_name,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return {'orders': list(orders.values()), 'grand_total': f'{grand_total:.2f}'}

@app.route('/favicon.svg')
def favicon():
    # First SVG (shield lock)
    svg1 = """
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-shield-lock" viewBox="0 0 16 16">
        <path d="M9.5 6.5a1.5 1.5 0 0 1-1 1.415l.385 1.99a.5.5 0 0 1-.491.595h-.788a.5.5 0 0 1-.490[...]
