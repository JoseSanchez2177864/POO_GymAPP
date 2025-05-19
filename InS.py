import bcrypt
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.uix.modalview import ModalView
from ConBD import crear_conexion

Builder.load_file("InS.kv")

class InSp(Screen):
    def verificar_credenciales(self):
        nombre = self.ids.nombre_input.text
        contrasena = self.ids.contrasena_input.text

        conn = crear_conexion()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT u.Id, u.Nombre_Usuario, r.Rol 
            FROM usuarios u
            JOIN Usuario_Rol r ON u.Id = r.Usuario
            WHERE u.Nombre_Usuario = ? AND u.Contraseña = ?
        """, (nombre, contrasena))
        
        resultado = cur.fetchone()
        conn.close()

        if resultado:
            usuario_id, nombre_usuario, rol = resultado
            app = App.get_running_app()
            app.usuario_id = usuario_id        # Guardar ID del usuario
            app.usuario_actual = nombre_usuario
            app.rol_actual = rol
            app.es_nuevo = False
            self.manager.current = "pantalla3"
        else:
            self.mostrar_error("Usuario o contraseña incorrecta")

    def mostrar_error(self, mensaje):
        layout = BoxLayout(orientation="vertical", spacing=15, padding=20)

        titulo = MDLabel(
            text="Error de inicio de sesión",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 0.3, 0.3, 1),
            bold=True,
            font_style="H6"
        )

        cuerpo = MDLabel(
            text=mensaje,
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.9),
        )

        cerrar_btn = MDRaisedButton(
            text="Cerrar",
            md_bg_color=(0.8, 0.1, 0.1, 1),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: popup.dismiss()
        )

        layout.add_widget(titulo)
        layout.add_widget(Widget(size_hint_y=None, height=10)) 
        layout.add_widget(cuerpo)
        layout.add_widget(Widget(size_hint_y=None, height=10))
        layout.add_widget(cerrar_btn)

        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint=(None, None),
            size=(dp(280), dp(200)),
            md_bg_color=(0.2, 0.2, 0.2, 0.85),
            radius=[20, 20, 20, 20]
        )
        card.add_widget(layout)

        popup = ModalView(
            size_hint=(None, None),
            size=(dp(300), dp(220)),
            background_color=(0, 0, 0, 0.7),
            auto_dismiss=True
        )
        popup.add_widget(card)
        popup.open()
