from app import app
from models import db

app.secret_key = 'abhishekbiswal123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://abhishekbiswal:idontknowpassword@localhost/namanyayg_clients_rostergram'
db.init_app(app)
