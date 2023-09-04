from flask import Flask, redirect, url_for, request, render_template


app = Flask(__name__)

@app.route('/')
def root():
    return 'Hello World!'

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')

@app.route('/transfer/confirm', methods=['POST'])
def verify():
    return render_template('verify.html', data=request.form)

@app.route('/transfer/confirm/complete', methods=['POST'])
def complete():
    return render_template('complete.html', data=request.form)


if __name__ == "__main__":
    app.run()