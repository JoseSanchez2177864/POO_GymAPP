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
        cur.execute("SELECT Contrasena FROM usuarios WHERE NombreUsuario = ?", (nombre,))
        row = cur.fetchone()
        conn.close()
        print(contrasena)
        if row and contrasena == row[0]:
            self.manager.current = "pantalla3"
        else:
            self.mostrar_error("Usuario o contraseña incorrecta")

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error de inicio de sesión',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()
