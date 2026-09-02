from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    isadmin = db.Column(db.Boolean, nullable=False, default=0)

    def set_password(self, passwordentry):
        """ Hash and store the password securely """
        self.password_hash = generate_password_hash(passwordentry)

    def check_password(self, passwordentry):
        """ Verify stored password hash against inputted password """
        return check_password_hash(self.password_hash, passwordentry)
    
    def __repr__(self):
        return '<User %r>' % self.id

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Product %r>' % self.id
    
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    users = db.relationship('Users', backref=db.backref('Orders', lazy=True)) #Foreign Key linking
    def __repr__(self):
        return '<Order %r>' % self.id

class Order_items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    orders = db.relationship('Orders', backref=db.backref('OrderItems'), lazy=True) 
    products = db.relationship('Products', backref=db.backref('OrderItems'), lazy=True)
    def __repr__(self):
        return '<Order Item %r>' % self.id

