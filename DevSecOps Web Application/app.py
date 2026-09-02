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
        <path d="M9.5 6.5a1.5 1.5 0 0 1-1 1.415l.385 1.99a.5.5 0 0 1-.491.595h-.788a.5.5 0 0 1-.49-.595l.384-1.99a1.5 1.5 0 1 1 2-1.415"/>
    </svg>
    """

    # Second SVG (cart)
    svg2 = """
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-cart" viewBox="0 0 16 16">
        <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5M3.102 4l1.313 7h8.17l1.313-7zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4m7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4m-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2m7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
    </svg>
    """

    # Combine the two SVGs
    combined_svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
        <g>{svg2}</g>
        <g transform="translate(0.5, 0.5)">{svg1}</g>
    </svg>
    """

    # Return the combined SVG as the response
    return Response(combined_svg, content_type="image/svg+xml")

@app.route('/')
def home():
    """ Directs to the home page where products can be viewed"""
    products = Products.query.all()
    for product in products:
        product.price = f"{product.price:.2f}"
    return render_template('home.html', products=products)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:  # You must be signed in to view your dashboard
        flash('You must sign in to view your dashboard', 'danger')
        return redirect(url_for('home'))
    products=Products.query.all()
    user_id = session.get('user_id')
    print("User Id:",user_id)
    user=Users.query.get(user_id)
    if user.isadmin:  # If the user is admin then all user data and order data can be viewed
        userslist=Users.query.all()
        userslist.remove(user)
        orders_details = []
        order_details = get_orders_summary(user_id)
        allordersquery = Orders.query.all()
        order_items = db.session.query(Order_items, Products.productname).join(Products, Order_items.product_id == Products.id).all()        
        products = Products.query.all()
        order_items_list = []
        for item, product_name in order_items:
            order_items_list.append({
                "order_id": item.order_id,
                "product_name": product_name,
                "quantity": item.quantity,
                "subtotal": f'{item.subtotal:.2f}'
            })
        
        grand_total = f'{sum(order.total_amount for order in allordersquery):.2f}'
        for u in userslist:
            orders_details.append(get_orders_summary(u.id))
        return render_template('account.html', order_details=order_details, all_orders=allordersquery, order_items=order_items_list, user=user, users=userslist,  grand_total=grand_total, products=products)
    else: # if user isn't admin then they can only view their own orders
        order_details = get_orders_summary(user_id)
    return render_template('account.html', order_details=order_details, user=user)

@app.route('/login', methods=['POST','GET'])
def login():
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))  # Redirect to the home or dashboard page

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if is_valid_email(email):
            user = Users.query.filter_by(email=email.strip().lower()).first()
        else:
            flash('Enter a valid email address!', 'danger')
            return redirect(url_for('login'))  # Redirect to the home or dashboard page
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['email'] = user.email
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/registeration', methods=['POST','GET'])
def registeration():
    if request.method == "POST":
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        
        if not is_valid_name(firstname):
            flash('First name must only contain alphabetic characters.', 'danger')
            return redirect(url_for('registeration'))
        
        if not is_valid_name(lastname):
            flash('Last name must only contain alphabetic characters.', 'danger')
            return redirect(url_for('registeration'))
        
        if not is_valid_email(email):
            flash('Invalid email address. Please provide a valid email.', 'danger')
            return redirect(url_for('registeration'))
        
        if not is_email_unique(email):
            flash('Email is already registered. Please use a different email.', 'danger')
            return redirect(url_for('registeration'))

        is_valid, error = is_valid_password(password)
        if not is_valid:
            flash(error, 'danger')
            return redirect(url_for('registeration'))
        
        new_user = Users(firstname=firstname.strip().capitalize(), lastname=lastname.strip().capitalize(),email=email.strip().lower())
        # file deepcode ignore DjangoUnvalidatedPassword: # Password is already validated with is_valid_password()
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except:
            flash('An error occurred. Please try again.', 'danger')
    else:
        return render_template('registeration.html')

@app.route('/view_cart')
def view_cart():
    if 'user_id' not in session:
        flash('You must log in to view and add to cart.', 'warning')
        return redirect(url_for('home'))
    cart = get_cart()
    for item in cart.get_items():
        price = item["price"]
        item["price"] = f"{price:.2f}"
        subtotal = item["subtotal"]
        item["subtotal"] = f"{subtotal:.2f}"
    cart.set_total(f"{cart.get_total():.2f}")
    print(cart.get_total())
    products = Products.query.all()
    for product in products:
        product.price = f"{product.price:.2f}"
    return render_template('view_cart.html', cart=cart, products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return redirect(url_for('home'))

    try:
        if 'user_id' not in session:
            flash('You must log in to add items to your cart.', 'warning')
            return jsonify({'status': 'error', 'message': 'You must log in to add items to your cart.'}), 401  

        product_id = request.json.get('product_id')
        product = Products.query.get(int(product_id))
        if not product:
            flash('There was an error identifying this product.', 'danger')
            return jsonify({'status': 'error', 'message': 'There was an error identifying this product.'}), 404

        if product.stock < 1:
            flash('This product is out of stock', 'danger')
            return jsonify({'status': 'error', 'message': 'This product is out of stock.'}), 400

        cart = get_cart()

        # Check current quantity of this product in cart
        current_quantity = cart.get_item_quantity(product_id)

        # If the quantity in cart + 1 exceeds stock, show an error
        if current_quantity + 1 > product.stock:
            flash(f'Only {product.stock} units available in stock.', 'danger')
            return jsonify({'status': 'error', 'message': f'Only {product.stock} units available in stock.'}), 400

        # Otherwise, add to cart
        print("Added to cart")
        cart.add_item(product_id, product.productname, 1, product.price)
        save_cart(cart)

        flash('Added to cart', 'success')
        return jsonify({'status': 'success', 'message': 'Added to cart'}), 200

    except Exception as e:
        flash("Some error occurred", 'danger')
        return jsonify({'status': 'error', 'message': 'Some error occurred', 'error': str(e)}), 500  

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'You must log in to modify the cart.'}), 401

    try:
        product_id = request.json.get('product_id')
        cart = get_cart()

        # Remove item from cart
        cart.remove_item(product_id)
        save_cart(cart)

        return jsonify({'success': True, 'message': 'Item removed from cart.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'You must log in to modify the cart.'}), 401

    try:
        cart = get_cart()
        cart.clear()  # Remove all items from cart
        save_cart(cart)

        return jsonify({'success': True, 'message': 'Cart emptied successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/get_cart_count', methods=['GET'])
def get_cart_count():
    if 'user_id' not in session:
        flash('You must log in to view and add to cart.', 'warning')
        return redirect(url_for('home'))
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return redirect(url_for('home'))
    cart = get_cart()
    total_items = sum(item['quantity'] for item in cart.get_items())
    print(total_items)
    return jsonify({'count': total_items})

@app.route('/checkout', methods=['POST','GET'])
def checkout():
    if 'user_id' not in session:
        flash('Signin to add items to cart and checkout!', 'danger')
        return redirect(url_for('home'))  # Redirect to the home or dashboard page
    cart = get_cart()
    products = Products.query.all()
    print("Total items in cart:", cart.get_total())
    if cart.get_total() == 0:
        flash('Cart is empty, nothing to checkout', 'warning')
        return redirect(url_for('home'))
    for item in cart.get_items():
        price = item["price"]
        item["price"] = f"{price:.2f}"
        subtotal = item["subtotal"]
        item["subtotal"] = f"{subtotal:.2f}"
    print(f"Total: {cart.get_total():.2f}")
    cart.set_total(f"{cart.get_total():.2f}")
    products = Products.query.all()
    for product in products:
        product.price = f"{product.price:.2f}"
    return render_template('checkout.html', cart=cart, products=products)

@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    if 'user_id' not in session:
        flash("You haven't logged in!", 'danger')
        return redirect(url_for('home'))  # Redirect to the home or dashboard page
    referer = request.headers.get('Referer')
    if not referer or '/checkout' not in referer:
        flash('Must complete checkout form to checkout!', 'danger')
        redirect(url_for('home'))
    try:
        user_id = session.get('user_id')
        cart = get_cart()
        new_order = Orders(customer_id=user_id, total_amount=cart.get_total(), order_date=datetime.now())
        db.session.add(new_order)
        db.session.commit()

        # Check if the product has enough stock
        for item in cart.get_items():
            product = Products.query.get(item['product_id'])
            if product.stock < item['quantity']:
                name = item["product_name"]
                flash(f'There are not enough {name}s in stock.', 'danger')
                redirect(url_for('view_cart'))
        for item in cart.get_items():
            product = Products.query.get(item['product_id'])
            # Deduct stock from the product
            product.stock -= item['quantity']
            # Add the item to the "Order_items" table
            order_item = Order_items(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )
            db.session.add(order_item)
        db.session.commit()
        empty_cart(cart)
        flash("Order successfully placed", "success")
        return redirect(url_for("dashboard"))
    
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback in case of database errors
        return jsonify({'error': 'An error occurred while processing your order', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        # Check if the user is logged in
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Unauthorised access'}), 403

        # Get the logged-in user's ID and fetch their record
        current_user_id = session.get('user_id')
        current_user = Users.query.get(current_user_id)

        if not current_user:
            return jsonify({'success': False, 'error': 'User not found in session'}), 404

        # Parse request data
        data = request.get_json()
        target_user_id = int(data.get('user_id'))  # ID of the user being updated
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')

        # Check if the target user exists
        target_user = Users.query.get(target_user_id)
        if not target_user:
            flash("User not found", 'danger')
            return jsonify({'success': False, 'error': 'User not found in session'}), 404  # Authorisation Logic
        if current_user.isadmin:
            # Admins can update any user's details
            pass
        elif current_user_id == target_user_id:
            # Regular users can only update their own details
            pass
        else:
            # Unauthorised access
            flash("You are not authorised to update this user's data", 'danger')
            return jsonify({'success': False, 'error': 'You are not authorized to update this user'}), 403
        # Update user details
        target_user.firstname = firstname
        target_user.lastname = lastname
        target_user.email = email

        # Commit changes to the database
        db.session.commit()
        flash("Updated details successfully", "success")
        return jsonify({'success': True, 'message': f"User {target_user.id}'s details updated successfully."})    
    except Exception as e:
    # Rollback in case of an error
        db.session.rollback()
        flash("Some error occured", "danger")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/change_password', methods=['POST'])
def change_password():
    try:
        # Get JSON data from the request
        data = request.get_json()
        user_id = data.get('user_id')
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        current_user_id = session.get('user_id')
        current_user = Users.query.get(current_user_id)
        # Validate inputs
        if (current_user.isadmin and user_id==current_user.id) or (not(current_user.isadmin) and user_id==current_user.id):
            if not (user_id and current_password and new_password):
                return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        else:
            if not (user_id and new_password):
                return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Fetch the user from the database
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404



        if (current_user.isadmin and user_id==current_user.id) or (not(current_user.isadmin) and user_id==current_user.id):
        # Verify the current password
            if not user.check_password(current_password):
                return jsonify({'success': False, 'error': 'Current password is incorrect'}), 403

            user.set_password(new_password)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Password updated successfully'})

        else:
            user.set_password(new_password)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Password updated successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/update_product', methods=['POST'])
def update_product():
    """ Method to update product details from input from the frontend"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        productname = data.get('productname')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock')

        # Fetch the product
        product = Products.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404

        # Update product details
        product.productname = productname
        product.description = description
        product.price = float(price)
        product.stock = int(stock)

        # Commit changes
        db.session.commit()

        return jsonify({'success': True, 'message': 'Product updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run()
