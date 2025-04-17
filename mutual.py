from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/mutual"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.secret_key = 'your_secret_key'  # Set a secret key for session management
db = SQLAlchemy(app)

class Mutual(db.Model):
    __tablename__ = 'fund'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

def load_scheme_data():
    # Load the entire dataset
    schemes = pd.read_csv('final_database.csv')
    # Filter for equity funds
    equity_schemes = schemes[schemes['category'] == 'Equity']
    return equity_schemes


@app.route("/", methods=['GET'])
def home():
    return render_template('practice.html')

@app.route("/container", methods=['GET', 'POST'])
def container():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')

    
        existing_user = Mutual.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for('login'))


        entry = Mutual(firstname=firstname, lastname=lastname, email=email, password=password)
        db.session.add(entry)
        db.session.commit()

        flash("User  registered successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('container.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Mutual.query.filter_by(email=email, password=password).first()
        if user :
            flash("Login successful!", "success")
            return redirect(url_for('home'))  # Redirect to home or dashboard
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template('login.html')
@app.route("/invest", methods=['GET','POST'])
def invest():
    
    return render_template('invest.html')

@app.route("/calculator", methods=['GET','POST'])
def calculator():
    
    return render_template('calculator.html')

@app.route("/FUNDS", methods=['GET','POST'])
def fund():
    
    return render_template('funds.html')

@app.route("/sip", methods=['GET','POST'])
def sip():
    schemes = load_scheme_data()
    scheme_names = schemes['scheme_name'].tolist() 
    result = None 
    user_inputs = {  
        'scheme_name': '',
        'monthly_investment': '',
        'years': '',
        'expected_return': '',
        'affecting_factor': ''
    }

    if request.method == 'POST':
        try:
            
            scheme_name = request.form.get('scheme_name')
            monthly_investment = request.form.get('monthly_investment')
            years = request.form.get('years')
            expected_return = request.form.get('expected_return')
            affecting_factor = request.form.get('affecting_factor')


            user_inputs = {
                'scheme_name': scheme_name,
                'monthly_investment': monthly_investment,
                'years': years,
                'expected_return': expected_return,
                'affecting_factor': affecting_factor
            }

            monthly_investment = float(monthly_investment)
            years = int(years)
            expected_return = float(expected_return)
            
            
            
            result = calculate_sip(monthly_investment, years, expected_return, affecting_factor, scheme_name, schemes)
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    return render_template('sip.html', scheme_names=scheme_names, result=result, user_inputs=user_inputs)

def calculate_sip(monthly_investment, years, expected_return, affecting_factor, selected_scheme, schemes):
    
    scheme_data = schemes[schemes['scheme_name'] == selected_scheme].iloc[0]

    
    total_investment = monthly_investment * 12 * years

    
    monthly_rate_of_return = expected_return / 100 / 12  
    n = years * 12 

    if monthly_rate_of_return > 0:
        future_value = monthly_investment * (np.power(1 + monthly_rate_of_return, n) - 1) / monthly_rate_of_return * (1 + monthly_rate_of_return)
    else:
        future_value = monthly_investment * n  

    profit = future_value - total_investment


    loss = 0
    if affecting_factor == 'yes':
        loss = (scheme_data['expense_ratio'] / 100) * future_value  

    final_amount_excluding_loss = future_value - loss

    return {
        "Invested Amount": f"₹{total_investment:.2f}",
        "Profit": f"₹{profit:.2f}",
        "Total Amount": f"₹{future_value:.2f}",
        "Loss": f"₹{loss:.2f}" if affecting_factor == 'yes' else "N/A",
        "Final Amount Excluding Loss": f"₹{final_amount_excluding_loss:.2f}" if affecting_factor == 'yes' else "N/A"

    }

@app.route("/scheme", methods=['GET','POST'])
def scheme():
    
    return render_template('scheme.html')

@app.route("/about", methods=['GET','POST'])
def about():
    
    return render_template('aboutus.html')

@app.route("/know", methods=['GET','POST'])
def know():
    
    return render_template('knowmore.html')

@app.route("/visual", methods=['GET','POST'])
def visual():
    
    return render_template('visualisation.html')

@app.route("/help", methods=['GET','POST'])
def help():
    
    return render_template('help&support.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
