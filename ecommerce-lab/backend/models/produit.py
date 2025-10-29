from backend.extensions import db

class Produit(db.model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'))
    images = db.relationship("ProduitImage", back_populates="produit", lazy=True)

class ProduitImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    produit = db.relationship("Produit", back_populates="images")

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    produits = db.relationship('Produit', backref='categorie', lazy=True)
    image_url = db.Column(db.String(255))
