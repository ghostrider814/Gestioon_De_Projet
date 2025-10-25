import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, redirect, url_for, request, Blueprint
from backend.models.product import Product
from backend.database import db
from backend.config import Config

# --------------------------
# Blueprint du panier
# --------------------------
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

# Panier en mémoire {product_id: quantity}
cart_data = {}

@cart_bp.route('/', methods=['GET', 'POST'])
def view_cart():
    global cart_data

    if request.method == 'POST':
        # Mise à jour des quantités depuis le formulaire
        for key, value in request.form.items():
            if key.startswith('qty_'):
                product_id = int(key.split('_')[1])
                qty = int(value)
                if qty > 0:
                    cart_data[product_id] = qty
                elif product_id in cart_data:
                    del cart_data[product_id]
        return redirect(url_for('cart.view_cart'))

    # Préparer les items pour le template
    cart_items = []
    total = 0
    for product_id, quantity in cart_data.items():
        product = Product.query.get(product_id)
        if product:
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=cart_items, total=total)

@cart_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    global cart_data
    if product_id in cart_data:
        cart_data[product_id] += 1
    else:
        cart_data[product_id] = 1
    return redirect(url_for('home'))

# --------------------------
# Application principale
# --------------------------
app = Flask(
    __name__,
    template_folder="templates",        # 📁 HTML ici
    static_folder="../frontend/assets"  # 📁 CSS et images ici
)

# Config Flask
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db.init_app(app)

# Register blueprint
app.register_blueprint(cart_bp)

# Liste de 50 produits pour insertion automatique
products_list = [
    ("T-shirt Rouge", 19.99), ("T-shirt Bleu", 19.99), ("T-shirt Vert", 19.99),
    ("Chaussures Running", 59.99), ("Chaussures Basket", 69.99), ("Chaussures Ville", 79.99),
    ("Casquette Rouge", 14.99), ("Casquette Bleue", 14.99), ("Casquette Noire", 14.99),
    ("Jean Slim", 39.99), ("Jean Regular", 39.99), ("Jean Noir", 42.99),
    ("Pull Col Rond", 29.99), ("Pull Col V", 29.99), ("Sweat Capuche", 34.99),
    ("Veste Cuir", 99.99), ("Veste Jeans", 89.99), ("Veste Hiver", 119.99),
    ("Chaussettes Courtes", 5.99), ("Chaussettes Longues", 6.99), ("Ceinture Cuir", 19.99),
    ("Sac à Dos", 49.99), ("Sac Bandoulière", 44.99), ("Pochette", 24.99),
    ("Montre Classique", 79.99), ("Montre Sport", 89.99), ("Lunettes Soleil", 29.99),
    ("Bonnet", 12.99), ("Écharpe", 14.99), ("Gants", 9.99),
    ("T-shirt Blanc", 19.99), ("T-shirt Noir", 19.99), ("T-shirt Gris", 19.99),
    ("Chaussures Été", 59.99), ("Chaussures Hiver", 69.99), ("Chaussures Printemps", 59.99),
    ("Casquette Été", 14.99), ("Casquette Hiver", 14.99), ("Casquette Sport", 14.99),
    ("Short Jean", 29.99), ("Short Sport", 24.99), ("Short Plage", 19.99),
    ("Chemise Blanche", 34.99), ("Chemise Bleu", 34.99), ("Chemise à Carreaux", 39.99),
    ("Veste Légère", 69.99), ("Veste Imperméable", 79.99), ("Veste Sport", 59.99),
    ("Pantalon Chino", 44.99), ("Pantalon Cargo", 49.99), ("Pantalon Sport", 39.99)
]

# Route accueil
@app.route('/')
def home():
    """Affiche la page d'accueil avec les produits"""
    products = Product.query.all()

    # Si la table est vide, ajouter les 50 produits
    if len(products) == 0:
        for name, price in products_list:
            db.session.add(Product(name=name, price=price))
        db.session.commit()
        products = Product.query.all()  # recharge tous les produits

    return render_template('index.html', products=products)

# --------------------------
# Lancer l'application
# --------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas
    app.run(debug=True)
