import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, render_template, redirect, url_for, request, session
from backend.models.product import Product

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

# --------------------------
# Panier
# --------------------------
@cart_bp.route('/', methods=['GET', 'POST'])
def view_cart():
    if 'cart' not in session:
        session['cart'] = []

    if request.method == 'POST':
        # Mise à jour des quantités
        for key, value in request.form.items():
            if key.startswith('qty_'):
                product_id = int(key.split('_')[1])
                qty = int(value)
                cart = session['cart']
                for item in cart:
                    if item['id'] == product_id:
                        if qty > 0:
                            item['quantity'] = qty
                        else:
                            cart.remove(item)
                        break
        session.modified = True
        return redirect(url_for('cart.view_cart'))

    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@cart_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        return redirect(url_for('home'))

    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']
    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += 1
            break
    else:
        cart.append({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': 1})

    session.modified = True
    return redirect(url_for('home'))
