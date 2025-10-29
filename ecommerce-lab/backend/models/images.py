from backend.extensions import db

class ProduitImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    produit = db.relationship("Produit", back_populates="images")