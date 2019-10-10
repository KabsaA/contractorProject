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
    'name' : 'Shirt',
    'title' : 'P!ATD T Shirt',
    'content' : '',
    'price' : 4
    },
    {
    'name' : 'Pants',
    'title' : 'Swe Pants',
    'content' : '',
    'price' : 35
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

@app.route('/inventory/add')
def item_add():
    title = "Add Item"
    return render_template('item_add.html', title=title, inventory={})

@app.route('/inventory', methods=['POST'])
def inventory_submit():
    '''Submit new item to inventory'''
    item = {
        'name': request.form.get('name'),
        "price": request.form.get('price'),
        'category': request.form.get('title'),
        'image': request.form.get('content')
    }

    item_id = inventory.insert_one(item).inserted_id
    return redirect(url_for('item_show', item_id=item_id))

@app.route('/inventory/<item_id>')
def item_show(item_id):
    '''Show single item'''
    item = inventory.find_one({'_id': ObjectId(item_id)})
    return render_template('item.html', item=item)

@app.route('/inventory/<item_id>/edit')
def item_edit(item_id):
    '''Show edit form for an item'''
    title = "Edit Item"
    item = inventory.find_one({'_id': ObjectId(item_id)})
    return render_template('item_edit.html', title=title, item=item)

@app.route('/inventory/<item_id>', methods=['POST'])
def item_update(item_id):
    '''Submit an edited item'''
    updated_item = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'category': request.form.get('category'),
        'image': request.form.get('image')
    }

    inventory.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})

    return redirect(url_for('item_show', item_id=item_id))

@app.route('/inventory/<item_id>/delete', methods=['POST'])
def item_delete(item_id):
    '''Delete item'''
    inventory.delete_one({'_id': ObjectId(item_id)})

    return redirect(url_for('show_admin'))

@app.route('/cart', methods=['POST'])
def add_to_cart():
    '''Submit new item to cart'''
    item = {
        'name': request.form.get('name'),
        "price": request.form.get('price'),
        'category': request.form.get('category')
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
