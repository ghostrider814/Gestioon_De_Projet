import os
from flask import Flask
from backend.extensions import db, migrate, login_manager, admin, csrf, compress, mail
from backend.config import Config

# Blueprints
from routes.produit import produit_bp
from routes.recherche import recherche_bp
from routes.categorie import categorie_bp
from routes.contact import contact_bp
from backend.routes.admin import admin_bp
from backend.routes.authentification import auth_bp
from backend.routes.commande import commande_bp
from backend.routes.paiement import paiement_bp

from backend.routes.panier import panier_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    admin.init_app(app)
    compress.init_app(app)
    mail.init_app(app)

    # Enregistrement des blueprints
    app.register_blueprint(produit_bp)
    app.register_blueprint(categorie_bp)
    app.register_blueprint(recherche_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(commande_bp)
    app.register_blueprint(paiement_bp)
    
    app.register_blueprint(panier_bp)

    return app

# Lancement local
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
