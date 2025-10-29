from flask import Blueprint, request, render_template, redirect, url_for
from flask_mail import Mail, Message
from flask import current_app as app

paiement_bp = Blueprint('paiement', __name__)
mail = Mail()

@paiement_bp.route('/paiement', methods=['GET'])
def paiement():
    return render_template('paiement.html')

@paiement_bp.route('/paiement/cash', methods=['POST'])
def paiement_cash():
    email = request.form.get('email')
    mode = "livraison"

    msg = Message(
        subject="Confirmation de votre commande",
        sender=("Boutique Paiement Fictif", app.config['MAIL_USERNAME']),
        recipients=[email],
        html=f"""
        <div style='font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4; border-radius: 10px;'>
          <h2 style='color: #007BFF;'>Confirmation de commande</h2>
          <p><strong>Commande :</strong> #123456</p>
          <p><strong>Montant :</strong> 250 MAD</p>
          <p><strong>Paiement :</strong> Espèces à la livraison</p>
          <hr style='margin: 20px 0;'>
          <p style='font-size: 14px; color: #555;'>Merci pour votre confiance.</p>
        </div>
        """
    )
    mail.send(msg)
    return redirect(url_for('paiement.paiement'))
