# app.py
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Cargamos el KV
Builder.load_file("Stats.kv")

# Definimos la primera pantalla
class Statsp(Screen):
    pass

