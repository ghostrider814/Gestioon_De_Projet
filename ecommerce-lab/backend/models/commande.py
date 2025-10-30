from datetime import datetime

class Commande(db.Model):
    __tablename__ = "commande"

    id = db.Column(db.Integer, primary_key=True)
    nom_client = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    pays = db.Column(db.String(50), nullable=True)
    commentaire = db.Column(db.Text, nullable=True)
    moyen_paiement = db.Column(db.String(30), nullable=False)
    total = db.Column(db.Float, nullable=False)
    statut = db.Column(db.String(20), default="en attente")
    date = db.Column(db.DateTime, default=datetime.utcnow)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    utilisateur = db.relationship('Utilisateur', backref='commandes')
    produits = db.relationship(
        'CommandeProduit',
        backref='commande',
        lazy=True,
        cascade="all, delete-orphan"
    )
