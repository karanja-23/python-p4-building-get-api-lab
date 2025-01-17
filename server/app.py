#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    body= '<h1>Bakeries</h1>'
    
    response = make_response(body, 200, {'Content-Type': 'text/html'})
    return response
@app.route('/bakeries')
def bakeries():
    bakeries_tuple =[]
    for bakery in Bakery.query.all():
        my_bakery = bakery.to_dict()
        bakeries_tuple.append(my_bakery)  
        
    response = make_response(bakeries_tuple, 200, {'Content-Type': 'application/json'})  
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    body = bakery.to_dict()
    
    response= make_response(body, 200, {'Content-Type':'application/json'})
    return response
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    obj= []
    for baked_good in BakedGood.query.order_by(BakedGood.price.desc()).all():
        obj.append(baked_good.to_dict())
    body = obj

    
    response = make_response(body, 200, {'Content-Type':'application/json'})
    return response
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    
    body = most_expensive_baked_good.to_dict()
    
    response = make_response(body, 200, {'Content Type':'application/json'})
    return response
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
