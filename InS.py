import bcrypt
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from ConBD import crear_conexion

Builder.load_file("InS.kv")

class InSp(Screen):
    def verificar_credenciales(self):
        nombre = self.ids.nombre_input.text
        contrasena = self.ids.contrasena_input.text

        conn = crear_conexion()
        cur = conn.cursor()
        cur.execute("""
    SELECT u.Nombre_Usuario, r.Rol 
    FROM usuarios u
    JOIN Usuario_Rol r ON u.Id = r.Usuario
    WHERE u.Nombre_Usuario = ? AND u.Contraseña = ?
""", (nombre, contrasena))

        resultado = cur.fetchone()

        if resultado:
            App.get_running_app().usuario_actual = resultado[0]
            App.get_running_app().rol_actual = resultado[1]
            App.get_running_app().es_nuevo = False
            self.manager.current = "pantalla3"

        else:
            self.mostrar_error("Usuario o contraseña incorrecta")

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error de inicio de sesión',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()
