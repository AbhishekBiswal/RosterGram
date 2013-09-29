from app import app
from models import db

app.secret_key = 'abhishekbiswal123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:abhishekbiswal@localhost/rg'
db.init_app(app)
