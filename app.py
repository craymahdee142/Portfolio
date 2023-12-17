from flask import Flask, url_for, redirect, make_response, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flaskapp.models.invoice import Invoice
#from flaskapp.models.user import User
#from flaskapp.models.invoice_manager import InvoiceManager
from datetime import datetime
from sqlalchemy import event, text, ForeignKey, asc
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, abort, current_app, session, flash
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from flask_login import login_required, current_user, LoginManager
from flask_login import logout_user, login_user, UserMixin
import uuid
import os
import logging
#import webview
# line 1
#from flaskwebgui import FlaskUI


app = Flask(__name__, static_url_path='/static')
bcrpyt = Bcrypt(app)

# line 2
#ui = FlaskUI(app, width=500, height=500)

#window = webview.create_window('VinartFooos', "http://127.0.0.1:5000/")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.rest'
app.config['SECRET_KEY'] = 'a7cf6260c9040b36a3e18473aa6e91ee7509'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://craydee:craymah1957@localhost/vinart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# Do not use this one
db = SQLAlchemy(app)
#db.init_app(app)
migrate = Migrate(app, db)

# Initialise flask login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader      
def load_user(user_id):
    return User.query.get(int(user_id))

# Sample product list
product_list = [
  { "code": "00", "name": "Jollof rice" },
  { "code": "01", "name": "Plain rice" },
  { "code": "02", "name": "Fried rice" },
  { "code": "03", "name": "Fufu" },
  { "code": "04", "name": "Kokonte" },
  { "code": "05", "name": "Banku" },
  { "code": "06", "name": "Rice ball" },
  { "code": "07", "name": "Tilapia" },
  { "code": "08", "name": "Dried Salmond" },
  { "code": "09", "name": "Fresh salmond" },
  { "code": "10", "name": "Poku fish" },
  { "code": "11", "name": "Red fish" },
  { "code": "12", "name": "Elban dried" },
  { "code": "13", "name": "Tuna" },
  { "code": "14", "name": "Goat meat" },
  { "code": "15", "name": "Cow meat" },
  { "code": "16", "name": "Chicken" },
  { "code": "17", "name": "Egg" },
  { "code": "18", "name": "Sobolo" },
  { "code": "19", "name": "Can malt" },
  { "code": "20", "name": "Can fanta" },
]

#Create tables
# Invoice class model
class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    prod_code = db.Column(db.String(20), nullable=False)
    prod_name = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    amt = db.Column(db.Float, nullable=False, default=0.0)
    total = db.Column(db.Float, nullable=False, default=0.0)
    date_created = db.Column(db.Date, default=datetime.utcnow().date())
    customer_id = db.Column(db.Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="invoices")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    user_fullname = db.Column(db.String(80))

    def __init__(self, prod_code, prod_name, price, qty, amt, total, user_id, user_fullname, customer=None):
        self.prod_code = prod_code
        self.prod_name = prod_name
        self.price = price
        self.qty = qty
        self.amt = amt
        self.total = total
        self.customer = customer
        self.user_id = user_id
        self.user_fullname=user_fullname

    def __repr__(self):
        return f"Invoice(id={self.id}, prod_code={self.prod_code}, prod_name={self.prod_name}, " \
               f"price={self.price}, qty={self.qty}, amt={self.amt}, total={self.total}, " \
               f"date_created={self.date_created})"


    def save(self):
        #Update at the current datetime
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance"""
        db.session.delete(self)
        db.session.commit()


@app.route("/generate_invoice", methods=['POST'])
def generate_invoice():
    # Retrieve cart data from the request
    cart_data = request.get_json()

    #customer_info = {}
    customer = None

    # Retreive or create the customer info
    #item_customer_info = cart_data[0].get('customer_info', {})
    #item_customer = get_or_create_customer(item_customer_info) if item_customer_info else None
    

    # Create and save invoices based on cart data
    invoices = []
    total_amount = 0.0

    for item in cart_data:
        if any(item.get(field) is None for field in ('prod_code', 'prod_name', 'price', 'amt')):
            flash(f"Warning: Some required fields are missing or incorrect in cart item: {item}")
            continue

        # Retrieve item details
        prod_code = item['prod_code']
        prod_name = item['prod_name']
        price = item['price']
        amt = item['amt']

        # Assuming qty is optional, set to 1 if not provided
        qty = item.get('qty', 1)
        if amt is not None:
            total_amount += amt

            # Get Customer info

            invoice_entry = Invoice(
                prod_code=prod_code,
                prod_name=prod_name,
                price=price,
                qty=qty,
                amt=amt,
                total=total_amount,
                #customer=item_customer, 
                # Add user_id and user fullname to the invoice
                user_id = current_user.id if current_user.is_authenticated else None,
                user_fullname = current_user.fullname if current_user.is_authenticated else None 
            )
            invoices.append(invoice_entry)
            db.session.add(invoice_entry)          

    try:
        db.session.commit()
        flash("Invoices generated and saved successfully.")
    except Exception as e:
        flash(f"Error committing to the database: {e}")
        db.session.rollback()

    # Get the list of invoices
    invoice_list = [{'prod_code': invoice.prod_code, 'prod_name': invoice.prod_name, 'price': invoice.price, 'qty': invoice.qty, 'amt': invoice.amt} for invoice in invoices]

    return jsonify({"success": True, "total": total_amount, "invoices": invoice_list})

# Route for invoice tables items
@app.route("/ord_line", methods=['GET'])
def invoice_page():
    # Fetch invoice from database by descending order
    invoice_entries = Invoice.query.order_by(asc(Invoice.date_created)).all()

    return render_template("ord_line.html", invoice_entries=invoice_entries)


# Reservation model
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=True)
    telephone_number = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    invoices = relationship("Invoice", back_populates="customer")

    def __repr__(self):
        return f"Customer(id={self.id}, customer_name={self.customer_name}, telephone_number={self.telephone_number}" \
            f"location={self.location}, description={self.description})"

# Route to save customer info
@app.route("/save_customer_info", methods=['POST'])
def save_customer_info():
    try:
        customer_info = request.get_json()
       
        required_fields = ['customer_name', 'telephone_number', 'location', 'description']
        if any(field not in customer_info for field in required_fields):
            return jsonify({'success': False, 'error': "Missing required fields"})

        # Create a new custmer or retrieve an existing one
        customer = Customer.query.filter_by(
            customer_name = customer_info.get('customer_name'),
            telephone_number = customer_info.get('telephone_number'),
            location = customer_info.get('location'),
            description = customer_info.get('description')
        ).first()

        if not customer:
            customer = Customer(**customer_info)
            db.session.add(customer)
            db.session.commit()
       
        session['customer_info'] = customer.id

        return jsonify({'success': True})
    except Exception as e:
        flash(f"Error saving customer information: {e}")
        return jsonify({'success': False})

def get_or_create_customer(customer_info, invoice_info=None):
    customer = Customer.query.filter_by(
        customer_name=customer_info.get('customer_name'),
        telephone_number=customer_info.get('telephone_number'),
        location=customer_info.get('location')
    ).first()

    if not customer:
        customer = Customer(**customer_info)
        db.session.add(customer)
        db.session.commit()

    if invoice_info:
        invoice_entry = Invoice(customer=customer, **invoice_info)
        db.session.add(invoice_entry)

    db.session.commit()

    return customer


# Get customer info
@app.route("/get_customer_info", methods=['GET'])
def get_customer_info():
    # Check if customer info is available in the session
    customer_id = session.get('customer_id')
    
    if customer_id:
        customer = Customer.query.get(customer_id)
        customer_info = {
            "customer_name": customer.customer_name,
            "telephone_number": customer.telephone_number,
            "location": customer.location,
            "description": customer.description
        }
    else:
        # Set default value if info not available
        customer_info ={"customer_name": " ", "telephone_number": " ", "location": " ", "description": " "}
    
    return jsonify(customer_info)



@app.route("/book_reserve", methods=['GET', 'POST'])
def book_reserve():
   if request.method == 'POST':
       # Retreive data from the request
       customer_name = request.form.get('customer_name')
       telephone_number = request.form.get('telephone_number')
       location = request.form.get('location')
       description = request.form.get('description')

       save_to_database(customer_name, telephone_number, location, description)

       #return jsonify({"success": True})
   
   return render_template("reserve.html")

def save_to_database(customer_name, telephone_number, location, description):
    try:
        # Create a new Customer instance
        customer = Customer(
            customer_name=customer_name,
            telephone_number=telephone_number,
            location=location,
            description=description
       )

        # Add the customer to the database session
        db.session.add(customer)

        # Commit the changes to the database
        db.session.commit()

        flash("Customer details saved successfully.")

    except Exception as e:
        flash(f"Error saving customer to the database: {e}")
        db.session.rollback()

# Income class
class Income(db.Model):
    __tablename__ = 'income'
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer)
    total = db.Column(db.Float, nullable=False, default=0.0)
    date_created = db.Column(db.Date, default=datetime.utcnow().date)

    def __repr__(self):
        return f"Income(id={self.id}, invoicce_id={self.invoice_id}, total={self.total}, " \
            f"date_created={self.date_created})"


    def save(self):
        #Update at the current datetime
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance"""
        db.session.delete(self)
        db.session.commit()

@event.listens_for(Invoice, 'after_insert')
# This is called after an invoice is created
def receive_after_insert(mapper, connection, target):
    try:    
        # Retreive the invoice details
        invoice_id = target.id
        total = target.total
        date_created = target.date_created

        # Create new invoice entry
        income_entry = Income(total=total, invoice_id=invoice_id, date_created=date_created)
        income_entry.updated_at = datetime.utcnow() 

        #with db.create_scoped_session() as new_session:
        #db.session.add(income_entry)
        #db.session.commit()
        # Create new income entry using parameterized query
        sql = text("INSERT INTO income (total, invoice_id, date_created) VALUES (:total, :invoice_id, :date_created)")
        params = {'total': total, 'invoice_id': invoice_id, 'date_created': date_created}
        connection.execute(sql, params)

        

    except SQLAlchemyError as e:
        logging.error(f"An error occured: str{(e)}")
        # Rollback the tramsaction
        db.session.rollback()
        return render_template("invoice.html", error_message="An error occured. Please again later")

# Route for the table items
@app.route("/income", methods=['GET'])
def income_page():
    # fetch income from the database
    income_entries = Income.query.all()

    return render_template("income.html", income_entries=income_entries)


# Expenses model class
class Expenses(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)    
    document_number = db.Column(db.Integer, unique=True, nullable=False)
    date_created = db.Column(db.Date, default=datetime.utcnow().date)
    description = db.Column(db.String(60), nullable=False)
    total = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Expenses(id={self.id}, document_number={self.document_number}, date_created={self.date_created}, description={self.description}, " \
            f"total={self.total})"

    def save(self):
        #Update at the current datetime
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance"""
        db.session.delete(self)
        db.session.commit()


# Route for the table items
@app.route("/expenses_bookings")
def expenses_booking_page():
    # fetch expenses data from the database
    expenses_bookings = Expenses.query.all()

    return render_template("expenses_bookings.html", expenses_bookings=expenses_bookings)


# Receivables model class
class Receivables(db.Model):
    __tablename__ = 'receivables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_number = db.Column(db.Integer, unique=True, nullable=False)
    date_created = db.Column(db.Date, default=datetime.utcnow().date)
    description = db.Column(db.String(60), nullable=False)
    total = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Receivables(id={self.id}, document_number={self.document_number}, date_created={self.date_created}, description={self.description}, " \
            f"total={self.total})"

    def save(self):
        #Update at the current datetime
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance"""
        db.session.delete(self)
        db.session.commit()


# Payables model class
class Payables(db.Model):
    __tablename__ = 'payables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_number = db.Column(db.Integer, unique=True, nullable=False)
    date_created = db.Column(db.Date, default=datetime.utcnow().date)
    description = db.Column(db.String(60), nullable=False)
    total = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Payables(id={self.id}, document_number={self.document_number}, date_created={self.date_created}, description={self.description}, " \
            f"total={self.total})"
    
    def save(self):
        #Update at the current datetime
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance"""
        db.session.delete(self)
        db.session.commit()


# Cask at bank model class
class CashBalance(db.Model):
    __tablename__ = 'cash_balance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_number = db.Column(db.Integer, unique=True, nullable=False)
    date_created = db.Column(db.Date, default=datetime.utcnow().date)
    description = db.Column(db.String(60), nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)
    
    def __repr__(self):
        return f"CashBalance(id={self.id}, document_number={self.document_number}, date_created={self.date_created}, description={self.description}, " \
            f"total={self.total})"


    def save(self):
        #Update at the current datetime
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance"""
        db.session.delete(self)
        db.session.commit()

"""Changed the naming for amount in  expenses, receivables, 
    payables & cash at bank for it to tally with the naming total in the Income model"""
def post_transaction(document_number, total, description, account):
    # Create transaction object 
    if account == 'expenses':
        transaction = Expenses(document_number=document_number, total=total, description=description)
    elif account == 'receivables':
        transaction = Receivables(document_number=document_number, total=total, description=description)
    elif account == 'payables':
         transaction = Payables(document_number=document_number, total=total, description=description)
         
    elif account == 'cashBalance':
         transaction = CashBalance(document_number=document_number, total=total, description=description)
    else:
        return jsonify({'error': 'Invalid account type'})
    # Created date
    transaction.date_created = datetime.utcnow().date()

    try:
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'success': 'Transaction posted successfully'})
    except Exception as e:
        db.session.rollback()
        print(f'Error: {str(e)}')
        return jsonify({'error':f'An error occured: {str(e)}'}), 500

# Endpoint to handle postings
@app.route("/post_transaction", methods=['POST'])
def handle_post_transaction():
    data = request.get_json()

    document_number = data.get('document_number')
    total = data.get('total')
    description = data.get('description')
    account = data.get('account')

    if not document_number or not total or not description:
        return jsonify({'error': 'Missing required data'})
    
    return post_transaction(document_number, total, description, account)

# Period route - For INCOME STATEMENT
@app.route("/period", methods=['GET'])
def period():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    return render_template("period.html", start_date=start_date, end_date=end_date)


# Income statement report
@app.route("/income_statement", methods=['POST'])
def income_statement():
    if request.method == 'POST':
        try:
            # Get the date for the report
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')

            # Query income and expenses with the selected range
            incomes = Income.query.filter(Income.date_created.between(start_date, end_date)).all()
            expenses = Expenses.query.filter(Expenses.date_created.between(start_date, end_date)).all()

            total_income = sum(income.total for income in incomes)
            total_expenses = sum(expense.total for expense in expenses)

            # Calculate net income
            net_income = total_income - total_expenses
            net_income = round(net_income, 2)

            # render the income statement  calculate values 
            return jsonify({"success": True, "total_income": total_income, "total_expenses": total_expenses, "net_income": net_income})
        except ValueError:
            # Handle invlalid date format
            return jsonify({"success": False, "error_message": "Invalid date format. Please use the format YYYY-MM-DD"})
    # If the request method is not POST, return an appropriate response
    return jsonify({"success": False, "error_message": "Invalid request method"})

    return render_template("period.hmtl")       

# Balance Period route - For FINANCIAL POSITION/BALANCE SHEET
@app.route("/balance_period", methods=['GET'])
def balance_period():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    return render_template("balance_period.html", start_date=start_date, end_date=end_date)


# Financial Position or Balance Sheet statement report
@app.route("/balance_sheet", methods=['POST'])
def balance_sheet():
    if request.method == 'POST':
        try:
            # Get the date for the report
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')

            # Query income and expenses with the selected range
            incomes = Income.query.filter(Income.date_created.between(start_date, end_date)).all()
            expenses = Expenses.query.filter(Expenses.date_created.between(start_date, end_date)).all()

            # Query receivables and payables with the selected range
            receivables = Receivables.query.filter(Receivables.date_created.between(start_date, end_date)).all()
            payables = Payables.query.filter(Payables.date_created.between(start_date, end_date)).all()

            total_income = sum(income.total for income in incomes)
            total_expenses = sum(expense.total for expense in expenses)

            total_receivables = sum(receivable.total for receivable in receivables)
            total_payables = sum(payable.total for payable in payables)

            # Calculate net income
            net_income = total_income - total_expenses
            net_income = round(net_income, 2)

            # Calculate financial position
            balance_sheet = ((total_receivables + net_income) - total_payables)

            # render the balance sheet with calculated values 
            return jsonify({"success": True, "total_receivables": total_receivables, "total_payables": total_payables, "net_income": net_income, "balance_sheet": balance_sheet})

        except ValueError:
            # Handle invalid date format
            return jsonify({"success": False, "error_message": "Invalid date format. Please use the format YYYY-MM-DD"})
    
    # If the request method is not POST, return an appropriate response
    return jsonify({"success": False, "error_message": "Invalid request method"})


# User model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)   
    fullname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def is_active(self):
        # Check if the account is marked  as active
        return self.active

    def __repr__(self):
        return f"('{self.username}', '{self.fullname}')"
   
    def save(self):
        #Update at the current datetime
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance"""
        db.session.delete(self)
        db.session.commit()

# Signup route
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        verify_password = request.form.get('verify_password')

        # Check password and password verify matches
        if password != verify_password:
            flash("Password do not match", "error")
            return redirect(url_for("signup"))
        # Hash the password
        hash_password = bcrpyt.generate_password_hash(password).decode("utf-8")

        #check if username is alraedy taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exist", "error")
            return render_template("signup.html")
        # Create new user
        new_user = User(username=username, password=hash_password, fullname=fullname)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Account created successfully", "success")
        return redirect(url_for("login"))
    # If request is not post, render the signup page
    return render_template("signup.html")

# Login in route
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username exist
        user = User.query.filter_by(username=username).first()

        if user and bcrpyt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username and password", "error")

    return render_template("login.html")

# dashboard route
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", "success")
    return redirect(url_for("home"))

# Import views
from flaskapp.views.home_view import*
from flaskapp.views.book_view import*
from flaskapp.views.payables_view import* 
from flaskapp.views.income_view import*
from flaskapp.views.ledger_view import*
from flaskapp.views.menu_view import*
from flaskapp.views.ord_view import*
from flaskapp.views.bookings_view import*
from flaskapp.views.login_view import*
from flaskapp.views.expenses_view import*
from flaskapp.views.receivables_view import*
from flaskapp.views.cashBalance_view import*
from flaskapp.views.invoice_view import*
#from flaskapp.views.invoice_page_view import*

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    #ui.run()
    #webview.start()

