# app.py
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.lang import Builder
import os

# Cargamos el KV
Builder.load_file("Inicio.kv")

class Iniciop(Screen):
    rol = NumericProperty(2)  # Rol por defecto (por ejemplo, 2 = usuario)

    def on_enter(self):
        app = App.get_running_app()
        self.rol = getattr(app, 'rol_actual', 2)  # Almacena el rol en la propiedad
        usuario = app.usuario_actual
        es_nuevo = getattr(app, 'es_nuevo', False)

        # Verificamos si la bienvenida ya fue mostrada para este usuario
        if not getattr(app, 'bienvenida_mostrada', False):
            if es_nuevo:
                mensaje = f"¡Hola {usuario}, gracias por registrarte! 🎉"
            else:
                if self.rol == 1:
                    mensaje = f"Bienvenido, {usuario} (Admin) 🛠️"
                elif self.rol == 2:
                    mensaje = f"Bienvenido de nuevo, {usuario} 👋"
                else:
                    mensaje = f"Bienvenido, {usuario} (Rol desconocido)"

            popup = Popup(
                title="Bienvenido",
                content=Label(text=mensaje),
                size_hint=(None, None), size=(400, 200)
            )
            popup.open()

            # Marcamos que la bienvenida ya fue mostrada
            app.bienvenida_mostrada = True

    def cerrar_sesion(self):
        app = App.get_running_app()
        app.bienvenida_mostrada = False  # Restablecemos para la próxima sesión
        app.usuario_actual = None
        app.root.current = 'pantalla1'  # Cambia al nombre de tu pantalla de login
    
