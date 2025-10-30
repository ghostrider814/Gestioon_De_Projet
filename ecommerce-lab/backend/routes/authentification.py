from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Utilisateur, db  # adapte selon ta structure (import de ton modèle et de db)

auth_bp = Blueprint('auth', __name__, template_folder='templates')


# ------------------------------------
# Route d'inscription (réservée aux CLIENTS)
# ------------------------------------
@auth_bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        # Vérifier si l'utilisateur existe déjà
        utilisateur_existant = Utilisateur.query.filter_by(email=email).first()
        if utilisateur_existant:
            flash("Un compte avec cet email existe déjà.", "warning")
            return redirect(url_for('auth.inscription'))

        # Créer un nouveau client
        mot_de_passe_hash = generate_password_hash(mot_de_passe)
        nouveau_client = Utilisateur(
            nom=nom,
            email=email,
            mot_de_passe=mot_de_passe_hash,
            role='client'  # Les admins ne s'inscrivent pas ici
        )

        db.session.add(nouveau_client)
        db.session.commit()

        flash("Inscription réussie. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('auth.connexion'))

    return render_template('auth/inscription.html')


# ------------------------------------
# Route de connexion (clients + admins)
# ------------------------------------
@auth_bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = Utilisateur.query.filter_by(email=email).first()

        if utilisateur and check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
            session['user_id'] = utilisateur.id
            session['role'] = utilisateur.role

            flash("Connexion réussie.", "success")

            if utilisateur.role == "admin":
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('categorie.accueil'))
        else:
            flash("Identifiants incorrects.", "danger")
            return redirect(url_for('auth.connexion'))

    return render_template('auth/connexion.html')


# ------------------------------------
# Route de déconnexion
# ------------------------------------
@auth_bp.route('/deconnexion')
def deconnexion():
    session.clear()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for('auth.connexion'))


# ------------------------------------
# Middleware utile : vérifie la connexion
# ------------------------------------
def utilisateur_connecte():
    return 'user_id' in session


def role_utilisateur():
    return session.get('role', None)
