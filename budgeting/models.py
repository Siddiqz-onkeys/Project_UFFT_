from config import db
from datetime import datetime

# User model
class User(db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Family model
class Family(db.Model):
    __tablename__ = "Families"
    family_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    family_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    primary_user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))

# Budget model
class Budget(db.Model):
    __tablename__ = "Budgets"
    budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    family_id = db.Column(db.Integer, db.ForeignKey("Families.family_id"), nullable=True)
    category = db.Column(db.String(255), nullable=False)
    budget_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    threshold_amount = db.Column(db.Float, default=0.0)  # Threshold for alert
    is_recurring = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BudgetAlert(db.Model):
    __tablename__ = "BudgetAlerts"
    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_id = db.Column(db.Integer, db.ForeignKey("Budgets.budget_id"))
    alert_type = db.Column(db.String(100))
    alert_message = db.Column(db.Text)
    alert_date = db.Column(db.DateTime, default=datetime.utcnow)

# Expense model
class Expense(db.Model):
    __tablename__ = "Expenses"
    expense_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_id = db.Column(db.Integer, db.ForeignKey("Budgets.budget_id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)  # Date is required
    description = db.Column(db.String(255))
    receipt_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
