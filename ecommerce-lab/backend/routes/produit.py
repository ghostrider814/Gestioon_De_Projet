from flask import Blueprint, render_template
from ..models import Produit

produit_bp = Blueprint('product', __name__)

@produit_bp.route('/produit/<int:id>')
def afficher_produit_carrousel(id):
    produit = Produit.query.get_or_404(id)
    return render_template('produit_carrousel.html', produit=produit)
