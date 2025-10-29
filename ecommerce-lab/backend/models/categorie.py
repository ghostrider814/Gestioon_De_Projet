from backend.extensions import db

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    produits = db.relationship('Produit', backref='categorie', lazy=True)
    image_url = db.Column(db.String(255))