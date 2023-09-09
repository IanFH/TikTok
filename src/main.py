from flask import Flask, redirect, url_for, request, render_template, session
from login_handler import LoginHandler
from urllib.parse import urlparse
from user import User
from user_credentials import UserCredentials
from topup_handler import TopUpHandler
from transaction_accumulator import TransactionAccumulator, FailsafeAccumulator
from transaction_task import TransactionTask
from bg_task_manager import BgTaskManager
from env import APP_SK
from database_handler import DatabaseHandler
from authenticator import Authenticator
import datetime


app = Flask(__name__)
app.secret_key = APP_SK
authenticator = Authenticator()
database_handler = DatabaseHandler()
transaction_accumulator = TransactionAccumulator()
failsafe_accumulator = FailsafeAccumulator()
bg_task_manager = BgTaskManager(transaction_accumulator, 
                                failsafe_accumulator, 
                                database_handler,
                                authenticator)
bg_task_manager.start()
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


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
    print(f"phone number: {request.form['phone_number']}")
    if request.form['password'] != request.form['confirm_password']:
        return redirect(url_for('register', err_msg='Passwords do not match'))
    if User.username_exists(database_handler, request.form['username']):
        return redirect(url_for('register', err_msg='Username already exists'))
    return render_template('register_confirm.html', data=request.form)

@app.route('/register/callback', methods=['GET','POST'])
def register_callback():
    print("CALLBACK")
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    phone_number = int(request.form['phone_number'].strip())
    ic_no = request.form['id'].strip()
    user = User.create_user(username, password, phone_number, ic_no)
    print(user)
    user.insert_to_database(database_handler)
    authenticator.add_user_credentials(UserCredentials(ic_no, ))
    print("INSERTED")
    return redirect(url_for("login"))

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
    user = login_handler.login(database_handler)
    if user:
        session['user'] = user.serialise()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login', err_msg='Invalid username or password'))

@app.route('/home')
def home():
    # TODO: Create HTML (Ian & Pandu)
    user_serialised = session.get('user', None)
    if user_serialised is None:
        return redirect(url_for('root'))
    user = User.deserialise(user_serialised)
    session['user'] = user.serialise()
    return render_template('home.html', user=user)

@app.route('/topup')
def topup():
    # user = User.deserialise(session['user'])
    user_serialised = session.get('user', None)
    if user_serialised is None:
        return redirect(url_for('root'))
    user = User.deserialise(user_serialised)
    url = f"https://buy.stripe.com/test_eVa6oJ7msgXi2QMbII?client_reference_id={user.get_uid()}"
    print(url)
    url = urlparse(f"https://buy.stripe.com/test_eVa6oJ7msgXi2QMbII?client_reference_id={user.get_uid()}").geturl()
    print(url)
    return redirect(url)

@app.route('/topup/success')
def topup_success():
    transaction_session_id = request.args.get('session_id', None)
    topup_handler = TopUpHandler(transaction_session_id)
    uid = topup_handler.process(transaction_accumulator)
    if uid is not None:
        user_data = database_handler.fetch_user_data_uid(uid)
        user = User.from_tuple(user_data)
        session['user'] = user.serialise()
        # TODO: Create HTML (Ian & Pandu)
        print(f"Success!")
        return render_template('topup_success.html')
    else:
        return redirect(url_for('topup_fail'))

@app.route('/topup/fail')
def topup_fail():
    # TODO: Create HTML (Ian & Pandu)
    user_serialised = session.get('user', None)
    if user_serialised is None:
        return redirect(url_for('root'))
    return render_template('topup_fail.html')

@app.route('/transfer')
def transfer():
    # TODO: Create HTML (Ian & Pandu)
    user_serialised = session.get('user', None)
    if user_serialised is None:
        return redirect(url_for('root'))
    user = User.deserialise(user_serialised)
    return render_template('transfer.html', user=user)

@app.route('/transfer/confirm', methods=['POST'])
def confirm():
    # TODO: Create HTML (Ian & Pandu)
    user_serialised = session.get('user', None)
    if user_serialised is None:
        return redirect(url_for('root'))
    user = User.deserialise(user_serialised)
    transfer_amount = request.form.get('amount', None)
    recipient_phone_number = request.form.get('phone_number', None)
    if transfer_amount == '' or recipient_phone_number == '':
        return redirect(url_for('transfer'))
    transfer_amount = float(transfer_amount)
    if transfer_amount > user.get_balance():
        return redirect(url_for('transfer', err_msg='Insufficient balance'))
    data = {
        'phone_number': recipient_phone_number,
        'amount': transfer_amount
    }
    return render_template('verify.html', data=data)

@app.route('/transfer/confirm/complete', methods=['POST'])
def complete():
    # TODO: Create HTML (Ian & Pandu)
    user_serialised = session.get('user', None)
    if user_serialised is None:
        return redirect(url_for('root'))
    user = User.deserialise(user_serialised)
    transfer_amount = request.form.get('amount', None)
    recipient_phone_number = request.form.get('phone_number', None)
    if transfer_amount is None or recipient_phone_number is None:
        return redirect(url_for('transfer'))
    transfer_amount = float(transfer_amount)
    user_recipient = database_handler.fetch_user_data_by_phone(recipient_phone_number)
    curr_datetime = datetime.datetime.now()
    transaction_task = TransactionTask(user.get_uid(), user_recipient[0], transfer_amount, curr_datetime)
    transaction_accumulator.add_transfer_task(transaction_task)
    data = {
            "transfer_amount": transfer_amount,
            "username": user_recipient[1],
            "balance": round(user.get_balance() - float(transfer_amount), 2)
        }
    return render_template('complete.html', data=data)

@app.route('/history')
def history():
    # TODO: Create HTML (Ian & Pandu)
    user_serialised = session.get('user', None)
    if user_serialised is None:
        return redirect(url_for('root'))
    return render_template('history.html')

@app.route('/history/details', methods=['POST'])
def history_details():
    # TODO: Create HTML (Ian & Pandu)
    HTML_DATE_FORMAT = "%Y-%m-%d"
    user_serialised = session.get('user', None)
    if user_serialised is None:
        return redirect(url_for('root'))
    start_date = request.form.get('start_date', None)
    end_date = request.form.get('end_date', None)
    if start_date is None or end_date is None:
        return redirect(url_for('history'))
    start_date = datetime.datetime.strptime(start_date, HTML_DATE_FORMAT)
    end_date = datetime.datetime.strptime(end_date, HTML_DATE_FORMAT)
    user = User.deserialise(session['user'])
    transaction_history = user.get_transaction_history(database_handler, start_date, end_date)
    return render_template('history_details.html', transaction_history=transaction_history)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('root'))

if __name__ == "__main__":
    app.run()