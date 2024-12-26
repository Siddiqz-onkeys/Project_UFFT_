from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "2003"
DB_NAME = "db1"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_secret_key"  # For session and flash messages

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
