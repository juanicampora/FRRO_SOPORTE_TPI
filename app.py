from flask import Flask,render_template, request, redirect, session,send_from_directory
from datetime import datetime
app=Flask(__name__, template_folder='./views/templates', static_folder='./views/static')
from controller import *
import db.funcionesdb as funcdb

if __name__ == '__main__':
    app.run(debug=True)
    