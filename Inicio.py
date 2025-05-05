# app.py
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Cargamos el KV
Builder.load_file("Inicio.kv")

# Definimos la primera pantalla
class Iniciop(Screen):
    pass

