from market import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(users_id):
    return Users.query.get(int(users_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)

    username = db.Column(db.String(length=20), nullable=False, unique=True)
    email_id = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    
    item = db.relationship('Items', backref='owned_user', lazy=True)
    
    def __repr__(self):
        return f"{self.username}, {self.email_id}, {self.id}"

    @property
    def prettier_budget(self):
        return f"{self.budget:,}$"
    
    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self, plain_pass):
        self.password = bcrypt.generate_password_hash(plain_pass, 10).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self, item_obj):
        return item_obj in self.item
    
    def add_budget(self, budget_obj):
        self.budget += budget_obj.add_budget.data
        db.session.commit()


class Items(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    
    owner = db.Column(db.Integer(), db.ForeignKey(Users.id))
    
    def __repr__(self):
        return f"{self.name}, {self.price}, {self.description}, {self.owner}"
    
    def buy(self, purchase_owner):
        self.owner = purchase_owner.id
        purchase_owner.budget-=self.price
        db.session.commit()

    def sell(self, sell_owner):
        self.owner = None
        sell_owner.budget += self.price
        db.session.commit()
    
    