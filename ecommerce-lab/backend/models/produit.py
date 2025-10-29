from backend.database import db

class Produit(db.Model):
    __tablename__ = 'produits'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100),nullable=False)
    prix = db.Column(db.Float,nullable=False)
