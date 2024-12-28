import os
from flask import Flask, render_template, request, redirect, flash,Blueprint
import mysql.connector
from datetime import datetime


budgeting_bp= Blueprint('budgeting', __name__)

'''# Flask app setup
app = Flask(__name__)
app.secret_key = "your_secret_key" '''

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2003",
        database="db1"
    )

# Routes
@budgeting_bp.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM budgets")
    budgets = cursor.fetchall()
    cursor.close()
    conn.close()
    print("Searching for templates in:", os.path.join(os.getcwd(), 'budgeting', 'templates'))
    #return render_template('home.html', budgets=budgets)
    try:
        return render_template('home.html',budgets=budgets)
    except Exception as e:
        return str(e)

@budgeting_bp.route('/add_budget', methods=['GET', 'POST'])
def add_budget():
    if request.method == 'POST':
        category = request.form['category']
        budget_amount = float(request.form['budget_amount'])
        threshold_amount = float(request.form['threshold_amount'])
        due_date = request.form['due_date']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Budget (category, budget_amount, threshold_amount, due_date, current_amount) "
            "VALUES (%s, %s, %s, %s, %s)",
            (category, budget_amount, threshold_amount, due_date, 0.0)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Budget added successfully!', 'success')
        return redirect('/')
    return render_template('add_budget.html')

@budgeting_bp.route('/expenses', methods=['GET', 'POST'])
def expenses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        budget_id = int(request.form['budget_id'])
        amount = float(request.form['amount'])
        description = request.form['description']
        date = request.form['date']
        
        if date:
            date = datetime.strptime(date, '%Y-%m-%d')
        else:
            date = datetime.now()
        
        cursor.execute("SELECT * FROM Budget WHERE budget_id = %s", (budget_id,))
        budget = cursor.fetchone()
        
        if not budget:
            flash("Budget not found!", "danger")
            return redirect('/expenses')

        # Add expense
        cursor.execute(
            "INSERT INTO Expense (budget_id, amount, description, date) VALUES (%s, %s, %s, %s)",
            (budget_id, amount, description, date)
        )
        conn.commit()

        # Update budget current amount
        new_current_amount = budget['current_amount'] + amount
        cursor.execute(
            "UPDATE Budget SET current_amount = %s WHERE budget_id = %s",
            (new_current_amount, budget_id)
        )
        conn.commit()

        # Check for threshold alert
        if new_current_amount > budget['threshold_amount']:
            alert_message = f"Alert: Your expenses for the {budget['category']} category have exceeded the threshold of ${budget['threshold_amount']}."
            cursor.execute(
                "INSERT INTO BudgetAlert (budget_id, alert_type, alert_message) VALUES (%s, %s, %s)",
                (budget_id, "Threshold Exceeded", alert_message)
            )
            conn.commit()

        flash('Expense added successfully!', 'success')
        return redirect('/expenses')

    cursor.execute("SELECT * FROM Budget")
    budgets = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('expenses.html', budgets=budgets)

@budgeting_bp.route('/report')
def report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get budgets and expenses
    cursor.execute("SELECT * FROM Budget")
    budgets = cursor.fetchall()
    cursor.execute("SELECT * FROM Expense")
    expenses = cursor.fetchall()
    
    # Calculate totals
    budget_expenses = {}
    for expense in expenses:
        if expense['budget_id'] not in budget_expenses:
            budget_expenses[expense['budget_id']] = 0
        budget_expenses[expense['budget_id']] += expense['amount']
    
    budget_details = []
    for budget in budgets:
        total_expenses = budget_expenses.get(budget['budget_id'], 0)
        remaining_budget = budget['budget_amount'] - total_expenses
        budget_details.append({
            'category': budget['category'],
            'budget_amount': budget['budget_amount'],
            'current_amount': budget['current_amount'],
            'total_expenses': total_expenses,
            'remaining_budget': remaining_budget,
            'due_date': budget['due_date']
        })
    
    cursor.close()
    conn.close()
    return render_template('report.html', budget_details=budget_details)

@budgeting_bp.route('/edit_budget/<int:budget_id>', methods=['GET', 'POST'])
def edit_budget(budget_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        category = request.form['category']
        budget_amount = float(request.form['budget_amount'])
        cursor.execute(
            "UPDATE Budget SET category = %s, budget_amount = %s WHERE budget_id = %s",
            (category, budget_amount, budget_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Budget updated successfully!', 'success')
        return redirect('/')
    
    cursor.execute("SELECT * FROM Budget WHERE budget_id = %s", (budget_id,))
    budget = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_budget.html', budget=budget)

# Run the budgeting_bp
if __name__ == '__main__':
    budgeting_bp.run(debug=True)
    #