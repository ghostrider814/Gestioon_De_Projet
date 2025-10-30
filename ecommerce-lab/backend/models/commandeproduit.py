from backend import db

class CommandeProduit(db.Model):
    __tablename__ = "commande_produit"

    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    statut = db.Column(db.String(20), default="en attente")

    produit = db.relationship('Produit')  # Accès à produit.nom, produit.prix
