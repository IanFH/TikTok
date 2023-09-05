from flask import Flask, redirect, url_for, request, render_template, session
from apscheduler.schedulers.background import BackgroundScheduler
from login_handler import LoginHandler
from urllib import parse
from user import User
from transaction_handler import TransactionHandler
from env import APP_SK
from database_handler import DatabaseHandler


app = Flask(__name__)
app.secret_key = APP_SK
background_scheduler = BackgroundScheduler()
database_handler = DatabaseHandler()


@app.route('/')
def root():
    # TODO: Create HTML (Ian & Pandu)
    return render_template('index.html')

@app.route('/register')
def register():
    # TODO: Create HTML (Ian & Pandu)
    err_msg = request.args.get('err_msg', None)
    return render_template('register.html', err_msg=err_msg)

@app.route('/register/confirm', methods=['POST'])
def register_confirm():
    # TODO: Create HTML (Ian & Pandu)
    if request.form['password'] != request.form['confirm_password']:
        return redirect(url_for('register', err_msg='Passwords do not match'))
    if User.username_exists(database_handler, request.form['username']):
        return redirect(url_for('register', err_msg='Username already exists'))
    return render_template('register_confirm.html', data=request.form)

@app.route('/register/callback', methods=['POST'])
def register_callback():
    username = request.form['username']
    password = request.form['password']
    user = User.create_user(username, password)
    user.insert_to_database(database_handler)
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
    session['user'] = user.serialise()
    return render_template('home.html', user=user)

@app.route('/topup')
def topup():
    # user = User.deserialize(session['user'])
    user = User(69, 'test_user')
    session['user'] = user.serialise()
    url = parse(f"https://buy.stripe.com/test_eVa6oJ7msgXi2QMbII?client_reference_id={user.get_uid()}")
    return redirect(url)

@app.route('/topup/success')
def topup_success():
    transaction_session_id = request.args.get('session_id', None)
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
    return render_template('history.html')

@app.route('/history/details')
def history_details():
    # TODO: Create HTML (Ian & Pandu)
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    user = User.deserialize(session['user'])
    transaction_history = user.get_transaction_history(database_handler, start_date, end_date)
    return render_template('history_details.html', transaction_history=transaction_history)

if __name__ == "__main__":
    app.run()