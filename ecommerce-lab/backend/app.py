import sys, os
from flask import Flask, redirect, url_for, request, Blueprint, send_from_directory, render_template_string
from backend.models.produit import Produit
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
panier_bp = Blueprint('panier', __name__, url_prefix='/panier')
panier_data = {}

@panier_bp.route('/', methods=['GET', 'POST'])
def voir_panier():
    """Affiche le panier"""
    global panier_data

    if request.method == 'POST':
        for key, value in request.form.items():
            if key.startswith('qty_'):
                produit_id = int(key.split('_')[1])
                qty = int(value)
                if qty > 0:
                    panier_data[produit_id] = qty
                elif produit_id in panier_data:
                    del panier_data[produit_id]
        return redirect(url_for('panier.voir_panier'))

    panier_items = []
    total = 0
    for produit_id, quantite in panier_data.items():
        produit = Produit.query.get(produit_id)
        if produit:
            sous_total = produit.price * quantite
            total += sous_total
            panier_items.append({
                'produit': produit,
                'quantite': quantite,
                'sous_total': sous_total
            })

    # Charger directement le fichier panier.html depuis frontend/
    with open(os.path.join(BASE_DIR, 'frontend', 'panier.html'), encoding='utf-8') as f:
        html = f.read()
    return render_template_string(html, panier_items=panier_items, total=total)


@panier_bp.route('/ajouter/<int:produit_id>')
def ajouter_au_panier(produit_id):
    """Ajoute un produit au panier"""
    global panier_data
    panier_data[produit_id] = panier_data.get(produit_id, 0) + 1
    return redirect(url_for('home'))


app.register_blueprint(panier_bp)

# --------------------------
# Produits (User Story 2)
# --------------------------
produits_list = [
    ("T-shirt Rouge", 19.99), ("Chaussures Running", 59.99),
    ("Casquette Noire", 14.99), ("Jean Slim", 39.99),
    ("Pull Col Rond", 29.99), ("Sweat Capuche", 34.99),
    ("Veste Cuir", 99.99), ("Bonnet", 12.99)
]

@app.route('/')
def home():
    """Page d'accueil sans templates/"""
    produits = Produit.query.all()

    if len(produits) == 0:
        for nom, prix in produits_list:
            db.session.add(Produit(name=nom, price=prix))
        db.session.commit()
        produits = Produit.query.all()

    with open(os.path.join(BASE_DIR, 'frontend', 'index.html'), encoding='utf-8') as f:
        html = f.read()
    return render_template_string(html, produits=produits)


# --------------------------
# Route statique (CSS, images)
# --------------------------
@app.route('/assets/<path:filename>')
def serve_static(filename):
    """Permet de charger CSS et images depuis frontend/assets"""
    return send_from_directory(os.path.join(BASE_DIR, 'frontend', 'assets'), filename)

from flask_mail import Mail
from backend.routes.checkout import checkout_bp, mail

app = Flask(__name__)
app.config.from_object('config')
mail.init_app(app)

app.register_blueprint(checkout_bp)

# Lancer l'application
# --------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


