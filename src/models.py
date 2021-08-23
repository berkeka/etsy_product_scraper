from app import db

class ProductsModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    image_url = db.Column(db.String())
    price = db.Column(db.Float())

    def __init__(self, name, image_url, price):
        self.name = name
        self.image_url = image_url
        self.price = price

    def __repr__(self):
        return f"<Car {self.name}>"