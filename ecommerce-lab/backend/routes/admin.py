from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.models import db, Produit, Categorie

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Page de gestion des produits
@admin_bp.route('/produits')
def gerer_produits():
    page = request.args.get("page", 1, type=int)
    produits = Produit.query.all().paginate(page=page, per_page=10)
    return render_template('admin/liste_des_produits.html', produits=produits)

# Page de gestion des catégories
@admin_bp.route('/categories')
def gerer_categories():
    page = request.args.get("page", 1, type=int)
    categories = Categorie.query.all().paginate(page=page, per_page=10)
    return render_template('admin/liste_des_categories.html', categories=categories)

# Ajouter un produit
@admin_bp.route('/produits/ajouter', methods=['GET', 'POST'])
def ajouter_produit():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        prix = request.form['prix']
        categorie_id = request.form['categorie_id']
        produit = Produit(nom=nom, description=description, prix=prix, categorie_id=categorie_id)
        db.session.add(produit)
        db.session.commit()
        flash("Produit ajouté avec succès !")
        return redirect(url_for('admin.gerer_produits'))
    categories = Categorie.query.all()
    return render_template('admin/ajouter_produit.html', categories=categories)

# Supprimer un produit
@admin_bp.route('/produits/supprimer/<int:id>', methods=['POST'])
def supprimer_produit(id):
    produit = Produit.query.get_or_404(id)
    db.session.delete(produit)
    db.session.commit()
    flash("Produit supprimé.")
    return redirect(url_for('admin.gerer_produits'))

# Ajouter une catégorie
@admin_bp.route('/categories/ajouter', methods=['GET', 'POST'])
def ajouter_categorie():
    if request.method == 'POST':
        nom = request.form['nom']
        categorie = Categorie(nom=nom)
        db.session.add(categorie)
        db.session.commit()
        flash("Catégorie ajoutée avec succès !")
        return redirect(url_for('admin.gerer_categories'))
    return render_template('admin/ajouter_categorie.html')

# Supprimer une catégorie
@admin_bp.route('/categories/supprimer/<int:id>', methods=['POST'])
def supprimer_categorie(id):
    categorie = Categorie.query.get_or_404(id)
    db.session.delete(categorie)
    db.session.commit()
    flash("Catégorie supprimée.")
    return redirect(url_for('admin.gerer_categories'))

# Modifier produit
@admin_bp.route('/produits/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_produit(id):
    produit = Produit.query.get_or_404(id)
    if request.method == 'POST':
        produit.nom = request.form['nom']
        produit.description = request.form['description']
        produit.prix = float(request.form['prix'])
        produit.categorie_id = int(request.form['categorie_id'])
        db.session.commit()
        flash("Produit modifié avec succès !")
        return redirect(url_for('admin.gerer_produits'))
    categories = Categorie.query.all()
    return render_template('admin/modifier_produit.html', produit=produit, categories=categories)

#Modifier categorie
@admin_bp.route('/categories/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_categorie(id):
    categorie = Categorie.query.get_or_404(id)
    if request.method == 'POST':
        categorie.nom = request.form['nom']
        db.session.commit()
        flash("Catégorie modifiée avec succès !")
        return redirect(url_for('admin.gerer_categories'))
    return render_template('admin/modifier_categorie.html', categorie=categorie)
