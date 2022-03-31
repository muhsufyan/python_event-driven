from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import requests, json
from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
host='localhost'
port='3306'
driver= 'mysql'
username='root'
password = ''
database = 'product'
app.config["SQLALCHEMY_DATABASE_URI"] = f'{driver}://{username}:{password}@{host}:{port}/{database}'
CORS(app)
db = SQLAlchemy(app)

# agar data yg dlm json serialize tambah decorator berikut
@dataclass
class Product(db.Model):
    # # validasi
    # id = int
    # title = str
    # image = str
    # masukan ke db
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

def loop(data):
    return data.id, data.title, data.image

# agar data yg dlm json serialize tambah decorator berikut
@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route("/")
def index():
    return "hello"

@app.route("/api/product")
def showall():
    # datanya adlh suatu list
    query_data = Product.query.all()
    # print(query_data[0].title)
    return jsonify([loop(i) for i in query_data])
@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://localhost:8000/randomproduct/')
    json = req.json()
    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        # event menyukai produk
        publish('product_liked', id)
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        'message': 'success'
    })
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")