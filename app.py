from flask import Flask,render_template, request, redirect, session,send_from_directory
from datetime import datetime

app=Flask(__name__, template_folder='./views')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)