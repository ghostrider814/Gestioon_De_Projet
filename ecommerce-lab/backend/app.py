import sys, os
from flask import Flask, redirect, url_for, request, Blueprint, send_from_directory, render_template_string
from backend.models.product import Product
from backend.database import db
from backend.config import Config

# === Corrige le chemin pour bien importer les fichiers backend ===
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# === Définir le chemin de base ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# === Création de l'application Flask ===
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'frontend', 'assets')  # 📁 Dossier des fichiers CSS/images
)

# === Config de la base de données ===
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --------------------------
# Panier (User Story 8)
# --------------------------
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
cart_data = {}

@cart_bp.route('/', methods=['GET', 'POST'])
def view_cart():
    """Affiche le panier"""
    global cart_data

    if request.method == 'POST':
        for key, value in request.form.items():
            if key.startswith('qty_'):
                product_id = int(key.split('_')[1])
                qty = int(value)
                if qty > 0:
                    cart_data[product_id] = qty
                elif product_id in cart_data:
                    del cart_data[product_id]
        return redirect(url_for('cart.view_cart'))

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

    # Charger directement le fichier cart.html dans frontend/
    with open(os.path.join(BASE_DIR, 'frontend', 'cart.html'), encoding='utf-8') as f:
        html = f.read()
    return render_template_string(html, cart_items=cart_items, total=total)

@cart_bp.route('/add/<int:product_id>')
def add_to_cart(product_id):
    """Ajoute un produit au panier"""
    global cart_data
    cart_data[product_id] = cart_data.get(product_id, 0) + 1
    return redirect(url_for('home'))

app.register_blueprint(cart_bp)

# --------------------------
# Produits (User Story 2)
# --------------------------
products_list = [
    ("T-shirt Rouge", 19.99), ("Chaussures Running", 59.99),
    ("Casquette Noire", 14.99), ("Jean Slim", 39.99),
    ("Pull Col Rond", 29.99), ("Sweat Capuche", 34.99),
    ("Veste Cuir", 99.99), ("Bonnet", 12.99)
]

@app.route('/')
def home():
    """Page d'accueil sans templates/"""
    products = Product.query.all()

    if len(products) == 0:
        for name, price in products_list:
            db.session.add(Product(name=name, price=price))
        db.session.commit()
        products = Product.query.all()

    with open(os.path.join(BASE_DIR, 'frontend', 'index.html'), encoding='utf-8') as f:
        html = f.read()
    return render_template_string(html, products=products)

# --------------------------
# Route statique (CSS, images)
# --------------------------
@app.route('/assets/<path:filename>')
def serve_static(filename):
    """Permet de charger CSS et images depuis frontend/assets"""
    return send_from_directory(os.path.join(BASE_DIR, 'frontend', 'assets'), filename)

# --------------------------
# Lancer l'application
# --------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
