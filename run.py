from flask import Flask, request, render_template, redirect, url_for, session,flash,make_response
from Expense.app import expense_bp
from user_reg.main import user_reg_bp
from Saving.app import saving_bp
from budgeting.budgeting import budgeting_bp  
def create_app():
    app = Flask(__name__)

    app = Flask(__name__)
    app.secret_key = 'ProjectUFFT'

    @app.route('/')
    def home():
            return render_template('home1.html')
       
  


    app.register_blueprint(expense_bp, url_prefix='/expense')
    app.register_blueprint(user_reg_bp, url_prefix='/user_reg')
    app.register_blueprint(saving_bp, url_prefix='/saving')
    app.register_blueprint(budgeting_bp, url_prefix='/budgeting') 
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True,port=8080)
