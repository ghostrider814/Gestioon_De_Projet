from flask import Blueprint, render_template, request
from models import Produit

recherche_bp = Blueprint('search', __name__)

@recherche_bp.route('/recherche')
def recherche_mots_cles():
    q = request.args.get('q', '')
    produits = Produit.query.filter(Produit.nom.ilike(f"%{q}%")).all()
    return render_template('recherche-mots_clé.html', produits=produits, mot_cle=q)
