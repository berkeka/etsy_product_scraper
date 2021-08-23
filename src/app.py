from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *
from scraper import Scraper

@app.route('/products', methods=['POST', 'GET'])
def handle_products():
    if request.method == 'POST':
        url = request.form['product_url']
        name, image_url, price = Scraper.scrap(url)
        new_product = ProductsModel(name, image_url, price)
        db.session.add(new_product)
        db.session.commit()
        return {"message": f"product {new_product.name} has been created successfully."}

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

@app.route('/products/new')
def new_product():
    return render_template("new_product.html")

@app.route('/')
def hello():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)