import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, render_template, redirect, url_for, request, session
from backend.models.produit import Product

# --------------------------
# Blueprint du panier
# --------------------------
panier_bp = Blueprint('panier', __name__, url_prefix='/panier')

# --------------------------
# Gestion du panier
# --------------------------
@panier_bp.route('/', methods=['GET', 'POST'])
def voir_panier():
    if 'panier' not in session:
        session['panier'] = []

    if request.method == 'POST':
        # Mise à jour des quantités
        for key, value in request.form.items():
            if key.startswith('qty_'):
                produit_id = int(key.split('_')[1])
                quantite = int(value)
                panier = session['panier']
                for item in panier:
                    if item['id'] == produit_id:
                        if quantite > 0:
                            item['quantite'] = quantite
                        else:
                            panier.remove(item)
                        break
        session.modified = True
        return redirect(url_for('panier.voir_panier'))

    panier_items = session.get('panier', [])
    total = sum(item['prix'] * item['quantite'] for item in panier_items)
    return render_template('panier.html', panier_items=panier_items, total=total)


@panier_bp.route('/ajouter/<int:produit_id>')
def ajouter_au_panier(produit_id):
    produit = Product.query.get(produit_id)
    if not produit:
        return redirect(url_for('home'))

    if 'panier' not in session:
        session['panier'] = []

    panier = session['panier']
    for item in panier:
        if item['id'] == produit.id:
            item['quantite'] += 1
            break
    else:
        panier.append({
            'id': produit.id,
            'nom': produit.name,
            'prix': produit.price,
            'quantite': 1
        })

    session.modified = True
    return redirect(url_for('home'))

@panier_bp.route("/ajouter-au-panier-ajax", methods=["POST"])
def ajouter_au_panier_ajax():
    produit_id = int(request.form.get("produit_id"))
    produit = Product.query.get(produit_id)
    if not produit:
        return jsonify({"status": "error", "message": "Produit introuvable"})

    panier = session.get("panier", [])
    for item in panier:
        if item["id"] == produit.id:
            item["quantite"] += 1
            break
    else:
        panier.append({
            "id": produit.id,
            "nom": produit.nom,
            "prix": produit.prix,
            "quantite": 1
        })

    session["panier"] = panier
    session.modified = True
    return jsonify({"status": "success", "message": f"{produit.nom} ajouté au panier 💖"})
