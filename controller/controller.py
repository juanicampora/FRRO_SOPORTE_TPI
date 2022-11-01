from app import app
from views.templates import *
from flask import Flask,render_template, request, redirect, session,send_from_directory
from datetime import datetime

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/alta')
def alta():
    return render_template('alta.html')

@app.route('/baja')
def baja():
    return render_template('baja.html')

@app.route('/listado')
def listar():
    return render_template('listado.html')