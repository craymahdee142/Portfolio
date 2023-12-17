from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from app import app, db
#from app import app, InvoiceManager, Invoice
#from flaskapp.models import InvoiceManager, Invoice


"""
# placeholder function
def get_invoice_details(invoice_id):
   
    # retrieve details based on the provided invoice_id
    invoice = Invoice.query.filter_by(id=invoice_id).first()

    if invoice:
        return {
            'invoice_id': invoice.id,
            'total_amount': invoice.total_amount,
            'invoice_items': [
                {
                    'prod_code': item.prod_code,
                    'prod_name': item.prod_name,
                    'qty': item.quantity,
                    'price': item.price,
                    'total_amount': item.total_amount
                }
                for item in invoice.invoice_items
            ]
        }
    else:
        return None

# Retrive invoice from invoice manager
@app.route("/generate_invoice", strict_slashes=False, methods=["POST"])
def generate_invoice():
    try:
        if not request.is_json:
            raise ValueError("Invalid content-type. Expected 'application/json',")
        data = request.get_json()

        cart_items = data.get('cartItems', [])

        # unique cart_id
        cart_id = str(uuid.uuid4())
        invoice_manager = InvoiceManager(cart_id)
        invoice_id = invoice_manager.generate_invoice(cart_items)

        invoice_details = get_invoice_details(invoice_id)
        
        #print("Retrieved Invoice Details:", invoice_details)  # Add this line for debugging
        #if request.is_json:
        #    return jsonify({'status': 'success', 'invoice_id': invoice_id}), 200
        #else:
           # Return JSON res for non JSON response
        return jsonify({'status':'success', 'invoice_id': invoice_id})
        #return render_template("invoice.html", invoice_id=invoice_id)
    
    except Exception as e:
        error_message = f"Error processing cart items: {str(e)}"
        return jsonify({'status': 'error', 'message': error_message})

# 
@app.route("/invoice/<invoice_id>")
def view_invoice(invoice_id):
    # Retreive invoice details from data store
    invoice_details = get_invoice_details(invoice_id)

    if invoice_details:
        return render_template("invoice.html", status='success', invoice_details=invoice_details)
    else:
        return jsonify({'status': 'error', 'message': 'Invoice not found'})
                               
                               
"""

# Generate invoice route

"""def handle_invoice_actions():
    action = request.form.get('action')
    invoice_manager = InvoiceManager()
    try:
        if action == 'calculate':
            invoice_manager.calculate()
            return jsonify({"success": True})
        elif action == 'populate':
            invoice_manager.populate_product_name()
            return jsonify({"success": True, "prod_name": invoice_manager.prod_name})
        if action == 'add_data':
            response = invoice_manager.add_data()
            return response
        if action == 'generate_invoice':
            cart_data = invoice_manager.get_cart_data()
            total = sum(item["amt"] for item in cart_data)
            print("Received action:", action)
            return jsonify({"cart": cart_data, "total": total})
        else:
            return jsonify({'error': "Invalid action"}), 400
        
        result = calculate_some_value()
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})
"""
#Route to ord_line page
#@app.route("/ord_line", strict_slashes=False)
#def ord_line():
#    return render_template("ord_line.html")

#Route to invoice page
@app.route("/invoice", strict_slashes=False)
def invoice():
    return render_template("invoice.html")

#Route to receipt page
@app.route("/receipt", strict_slashes=False)
def _receipt():
    return render_template("receipt.html")

