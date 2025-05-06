# app.py
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder

# Cargamos el KV
Builder.load_file("Inicio.kv")

# Definimos la primera pantalla
class Iniciop(Screen):
    def on_enter(self):
        app = App.get_running_app()
        usuario = app.usuario_actual
        rol = getattr(app, 'rol_actual', 2)
        es_nuevo = getattr(app, 'es_nuevo', False)

        if es_nuevo:
            mensaje = f"¡Hola {usuario}, gracias por registrarte! 🎉"
        else:
            if rol == 1:
                mensaje = f"Bienvenido, {usuario} (Admin) 🛠️"
            elif rol == 2:
                mensaje = f"Bienvenido de nuevo, {usuario} 👋"
            else:
                mensaje = f"Bienvenido, {usuario} (Rol desconocido)"

        popup = Popup(
            title="Bienvenido",
            content=Label(text=mensaje),
            size_hint=(None, None), size=(400, 200)
        )
        popup.open()

