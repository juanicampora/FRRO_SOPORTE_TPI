from flask import Flask
from app.configuracion import Config
from app.routes.rutas import global_rutas


app=Flask(__name__, template_folder=Config.CARPETA_TEMPLATES, static_folder=Config.CARPETA_STATIC)
app.config.from_object(Config)

app.register_blueprint(global_rutas, url_prefix="/")

