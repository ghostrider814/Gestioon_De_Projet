from flask import Blueprint, render_template, request, session
from ..models import Categorie, Produit

categorie_bp = Blueprint('category', __name__)

@categorie_bp.route('/')
def accueil():
    categories = Categorie.query.all()
    panier = session.get('panier', [])
    panier_count = sum(item['quantite'] for item in panier)
    return render_template('accueil.html', categories=categories, panier_count=panier_count)

@categorie_bp.route('/categorie/<int:id>')
def produits_par_categorie(id):
    page = request.args.get("page", 1, type=int)
    categorie = Categorie.query.get_or_404(id)
    produits = Produit.query.filter_by(categorie_id=id).all().paginate(page=page, per_page=10)
    return render_template('category.html', categorie=categorie, produits=produits)
