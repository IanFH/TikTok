from flask import Flask, redirect, url_for, request, render_template, session
from login_handler import LoginHandler
from user import User
from transaction_handler import TransactionHandler
from env import APP_SK


app = Flask(__name__)
app.secret_key = APP_SK


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
        session['user'] = user.serialize()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login', err_msg='Invalid username or password'))

@app.route('/home')
def home():
    # TODO: Create HTML (Ian & Pandu)
    user = User.deserialize(session['user'])
    # some code logic (tbc)
    session['user'] = user.serialise()
    return render_template('home.html')

@app.route('/topup')
def topup():
    # user = User.deserialize(session['user'])
    user = User(69, 'test_user')
    session['user'] = user.serialise()
    url = f"https://buy.stripe.com/test_eVa6oJ7msgXi2QMbII?client_reference_id={user.get_uid()}"
    # TODO: Add safe url (Joseph)
    return redirect(url)

@app.route('/topup/success')
def topup_success():
    transaction_session_id = request.args.get('session_id', None)
    retrieved_uid = request.args.get('uid', None)
    transaction_handler = TransactionHandler(transaction_session_id)
    res = transaction_handler.process()
    if res:
        # TODO: Create HTML (Ian & Pandu)
        print(f"Success!")
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