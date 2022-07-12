import os
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    sdescription = db.Column(db.String(100), nullable=False)
    imageurl = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

@app.route('/')
def index():
    db.create_all()
    products = Product.query.all()
    return render_template('store.html',products=products)

@app.route('/create', methods=["GET","POST"])
def create():
    db.create_all()
    if request.method == 'POST':
        product = Product(name = request.form["name"],
                          price = request.form['price'],
                          description = request.form['description'],
                          sdescription = request.form['sdescription'],
                          imageurl = request.form['imageurl']
        )
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/product/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    return render_template("product.html", product=product)

@app.route('/cart', methods = ['GET','POST'])
def cart():
    if not session.get("cart"):
        session['cart'] = []
    cart = session['cart']
    products = []
    for product in cart:
        p = Product.query.get_or_404(product)
        products.append(p)
    if len(products) == 0:
        flash("سبد خرید شما خالی است")
    return render_template('cart.html', cart=products)

@app.route('/cart/add', methods = ['GET','POST'])
def cartadd():
    if request.method == 'POST':
        if not session.get('cart'):
            session['cart'] = []
        session['cart'].append(request.form['id'])
        flash("محصول به سبد خرید شما اضافه شد")
        return redirect(url_for('cart'))


@app.route('/cart/remove', methods = ['GET','POST'])
def cartremove():
    if request.method == 'POST':
        session['cart'].remove(request.form['id'])
        flash("محصول از سبد خرید شما حذف شد")
        return redirect(url_for('cart'))