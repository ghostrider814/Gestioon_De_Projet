from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Utilisateur(db.Model):
    __tablename__ = "utilisateur"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="client")  # "client" ou "admin"

    commandes = db.relationship("Commande", backref="utilisateur", lazy=True)
