from flask import Flask, redirect, url_for, request, render_template
from login_handler import LoginHandler
from user import User
from transaction_handler import TransactionHandler


app = Flask(__name__)

@app.route('/')
def root():
    # TODO: Create HTML (Ian & Pandu)
    return render_template('index.html')

@app.route('/register')
def register():
    # TODO: Create HTML (Ian & Pandu)
    return render_template('register.html')

@app.route('/register/confirm', methods=['POST'])
def register_confirm():
    # TODO: Create HTML (Ian & Pandu)
    return render_template('register_confirm.html', data=request.form)

@app.route('/register/callback', methods=['POST'])
def register_callback():
    # TODO: Implement registration (Marcus)
    # Use the User class to create a new user and insert it into the database
    return redirect(url_for("root"))

@app.route('/login')
def login():
    # TODO: Create HTML (Ian & Pandu)
    return render_template('login.html')

@app.route('/login/callback', methods=['POST'])
def login_callback():
    """
    Handles the login process
    """
    login_handler = LoginHandler(request.form['username'], request.form['password'])
    user = login_handler.login()
    if user:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login', err_msg='Invalid username or password'))

@app.route('/home')
def home():
    # TODO: Create HTML (Ian & Pandu)
    return render_template('home.html')

@app.route('/topup')
def topup():
    # TODO: Create HTML (Ian & Pandu)
    # Page should redirect to this URL: https://buy.stripe.com/test_eVa6oJ7msgXi2QMbII
    return render_template('topup.html')

@app.route('/topup/success')
def topup_success():
    transaction_session_id = request.args.get('session_id', None)
    res = TransactionHandler.process(transaction_session_id)
    if res:
        # TODO: Create HTML (Ian & Pandu)
        return render_template('topup_success.html')
    else:
        return redirect(url_for('topup_fail'))

@app.route('/topup/fail')
def topup_fail():
    # TODO: Create HTML (Ian & Pandu)
    return render_template('topup_fail.html')

@app.route('/transfer')
def transfer():
    # TODO: Create HTML (Ian & Pandu)
    # TODO: Implement get contacts (Joseph)
    return render_template('transfer.html')

@app.route('/transfer/confirm', methods=['POST'])
def confirm():
    # TODO: Create HTML (Ian & Pandu)
    return render_template('verify.html', data=request.form)

@app.route('/transfer/confirm/complete', methods=['POST'])
def complete():
    # TODO: Create HTML (Ian & Pandu)
    return render_template('complete.html', data=request.form)

@app.route('/history')
def history():
    # TODO: Create HTML (Ian & Pandu)
    # TODO: Get transaction history (Joseph)
    return render_template('history.html', data=request.form)

if __name__ == "__main__":
    app.run()