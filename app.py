from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/db')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items
cart = db.cart

items.drop()
cart.drop()


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
    }
])

@app.route('/cart')
def cart():
    return render_template("cart.html" , title='Cart')

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

@app.route('/items/add')
def item_add():
    title = "add item to cart"
    return render_template('cart.html', title=title, items={})

@app.route('/add', methods=['POST'])
def add_item():
    '''Submit new item to inventory'''
    item = {
        'name': request.form.get('name'),
        "price": request.form.get('price'),
        'title': request.form.get('title'),
        'content': request.form.get('content')
    }

    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('show_cart', item_id=item_id))

@app.route('/items/<item_id>')
def item_show(item_id):
    '''Show single item'''
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item.html', item=item)

@app.route('/items/<item_id>/edit')
def item_edit(item_id):
    '''Show edit form for an item'''
    title = "Edit Item"
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item_edit.html', title=title, item=item)

@app.route('/items/<item_id>', methods=['POST'])
def item_update(item_id):
    '''Submit an edited item'''
    updated_item = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'title': request.form.get('title'),
        'content': request.form.get('content')
    }

    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})

    return redirect(url_for('item_show', item_id=item_id))

@app.route('/inventory/<item_id>/delete', methods=['POST'])
def item_delete(item_id):
    '''Delete item'''
    items.delete_one({'_id': ObjectId(item_id)})


@app.route('/cart/<item_id>/', methods=['POST'])
def add_to_cart():
    '''Submit new item to cart'''
    item = {
        'name': request.form.get('name'),
        "price": request.form.get('price'),
        'title': request.form.get('title')
    }

    add_item = items.insert_one(item).inserted_id
    return redirect(url_for('show_cart', add_item=add_item))

@app.route('/cart/<item_id>/delete', methods=['POST'])
def remove_from_cart(item_id):
    '''Remove item from cart'''
    cart.delete_one({'_id': ObjectId(item_id)})

    return redirect(url_for('show_cart'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
