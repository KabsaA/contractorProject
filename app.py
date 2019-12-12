from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/contractorProject')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items
cart = db.cart

items.drop()
cart.drop()

app = Flask(__name__)
items.insert_many([
    {
    'name' : 'P!ATD T SHIRT',
    'title' : 'Mens T Shirt',
    'content' : 'static/images/patd.jpg',
    'price' : 25
    },
    {
    'name' : 'FALL OUT BOY',
    'title' : 'Womens T Shirt',
    'content' : 'static/images/fob.jpg',
    'price' : 35
    },
    {
    'name' : '21 PILOTS',
    'title' : 'T Shirt',
    'content' : 'static/images/21pilots.jpg',
    'price' : 30
    },
    {
    'name' : 'THE 1975',
    'title' : 'Unisex: T Shirt',
    'content' : 'static/images/the1975.jpg',
    'price' : 30
    }
])



@app.route('/')
def home():
    """Show all inventory."""
    # This will display all inventory by looping through the database
    return render_template('home.html', items=items.find())

@app.route('/cart')
def show_cart():
    """Show cart."""
    carts = cart.find()

    return render_template('cart.html', cart=carts)



@app.route('/cart/<item_id>/add', methods=['POST'])
def add_to_cart(item_id):
    '''Submit new item to cart'''
    item = {
        'name': request.form.get('name'),
        "price": request.form.get('price'),
        'title': request.form.get('title')
    }

    add_item = cart.insert_one(item).inserted_id
    return redirect(url_for('show_cart', add_item=add_item))

@app.route('/cart/<item_id>/delete', methods=['POST'])
def remove_from_cart(item_id):
    '''Remove item from cart'''
    cart.delete_one({'_id': ObjectId(item_id)})

    return redirect(url_for('show_cart'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
