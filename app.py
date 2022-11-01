import controller.controller
from flask import Flask,render_template, request, redirect, session,send_from_directory
from datetime import datetime

app=Flask(__name__, template_folder='./views/templates', static_folder='./views/static',)


if __name__ == '__main__':
    app.run(debug=True)