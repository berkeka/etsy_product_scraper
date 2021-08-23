from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *
from scraper import Scraper

@app.route('/products', methods=['POST', 'GET'])
def handle_products():
    if request.method == 'POST':
        url = request.form['product_url']
        name, image_url, price, error = Scraper.scrap(url)
        if error != None:
            flash(error ,'error')
            return redirect(url_for('index'))
        else:
            new_product = ProductsModel(name, image_url, price)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('show_product', product_id = new_product.id))

    elif request.method == 'GET':
        products = ProductsModel.query.all()
        results = [
            {
                "id": product.id,
                "name": product.name,
                "image_url": product.image_url,
                "price": product.price
            } for product in products]

        return render_template("products.html", products = results)

@app.route('/products/<int:product_id>')
def show_product(product_id):
    product = ProductsModel.query.get(product_id)
    if product is None:
        return render_template("404.html")
    return render_template("product.html", product = product)

@app.route('/products/new')
def new_product():
    return render_template("new_product.html")

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)