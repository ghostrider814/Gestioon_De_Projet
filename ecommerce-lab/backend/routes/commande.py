from flask import Blueprint, request, redirect, url_for, session, flash, render_template
from backend.models.commande import Commande, CommandeProduit
from backend.models.produit import Produit
from backend.models.utilisateur import Utilisateur
from backend.database import db
from flask_mail import Message, Mail
from flask import current_app as app
from datetime import datetime
import re

commande_bp = Blueprint('commande', __name__, url_prefix='/commande')

def email_valide(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def telephone_valide(numero):
    return re.match(r"^\+?\d{9,15}$", numero)

@commande_bp.route('/valider', methods=['POST'])
def valider_commande():
    panier = session.get("panier", [])
    if not panier:
        flash("Votre panier est vide.")
        return redirect(url_for("cart.afficher_panier"))

    client_id = session.get("user_id")
    client = Utilisateur.query.get(client_id)

    if not client:
        flash("Vous devez être connecté pour passer commande.")
        return redirect(url_for("auth.connexion"))

    nom = client.nom
    email = client.email
    telephone = request.form.get("telephone")
    moyen = request.form.get("moyen_paiement")
    commentaire = request.form.get("commentaire")

    if not telephone_valide(telephone):
        flash("Numéro de téléphone invalide.")
        return redirect(url_for("cart.afficher_panier"))

    total = sum(item["prix"] * item["quantite"] for item in panier)

    commande = Commande(
        nom_client=nom,
        email=email,
        telephone=telephone,
        moyen_paiement=moyen,
        commentaire=commentaire,
        total=total,
        statut="en attente",
        date=datetime.utcnow(),
        utilisateur_id=client.id
    )
    db.session.add(commande)
    db.session.commit()

    for item in panier:
        ligne = CommandeProduit(
            produit_id=item["id"],
            commande_id=commande.id,
            quantite=item["quantite"]
        )
        db.session.add(ligne)

    db.session.commit()
    session["panier"] = []
    session.modified = True

    msg = Message(
        subject="Confirmation de votre commande – Celio's Shop",
        sender=("Celio's Shop", app.config['MAIL_USERNAME']),
        recipients=[email],
        html=f"""
        <div style='font-family: Segoe UI, sans-serif; padding: 20px; background-color: #f4f6f9; border-radius: 12px;'>
          <h2 style='color: #2c3e50;'>Bonjour {nom},</h2>
          <p>Nous avons bien reçu votre commande <strong>#{commande.id}</strong>.</p>
          <p><strong>Montant :</strong> {total:.2f} MAD</p>
          <p><strong>Moyen de paiement :</strong> {moyen}</p>
          <p><strong>Statut :</strong> {commande.statut}</p>
          <hr style='margin: 20px 0;'>
          <p style='font-size: 14px; color: #555;'>Merci pour votre confiance 💖</p>
        </div>
        """
    )
    try:
        Mail(app).send(msg)
    except Exception as e:
        print("Erreur envoi mail :", e)

    if moyen == "carte":
        return redirect("https://buy.stripe.com/test_4gM4gydGzaV23Z056RbAs00")
    elif moyen == "paypal":
        return redirect("https://www.paypal.com/ncp/payment/KJUDQMJPSCEU6")
    else:
        return redirect(url_for("public.accueil"))

# 🧾 Historique client
@commande_bp.route('/mes-commandes')
def mes_commandes():
    client_id = session.get("user_id")
    if not client_id:
        flash("Veuillez vous connecter pour voir vos commandes.")
        return redirect(url_for("auth.connexion"))

    commandes = Commande.query.filter_by(utilisateur_id=client_id).order_by(Commande.date.desc()).all()
    return render_template("client/mes_commandes.html", commandes=commandes)

# 📦 Suivi d’une commande
@commande_bp.route('/tracking/<int:id>')
def suivi_commande(id):
    client_id = session.get("user_id")
    commande = Commande.query.filter_by(id=id, utilisateur_id=client_id).first()

    if not commande:
        flash("Commande introuvable.")
        return redirect(url_for("commande.mes_commandes"))

    return render_template("client/tracking.html", commande=commande)
