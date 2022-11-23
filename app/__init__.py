from flask import Flask
from app.configuracion import Config
from app.routes.rutas import global_rutas
from flask_login import LoginManager

app=Flask(__name__, template_folder=Config.CARPETA_TEMPLATES, static_folder=Config.CARPETA_STATIC)
app.config.from_object(Config)

app.register_blueprint(global_rutas, url_prefix="/")

login_manager_app=LoginManager(app)

from app.routes.rutas import controlador

@login_manager_app.user_loader
def load_user(usuario):
    return controlador.devTrabajador(usuario)