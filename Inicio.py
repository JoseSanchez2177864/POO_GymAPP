from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivy.lang import Builder

Builder.load_file("Inicio.kv")


class Iniciop(Screen):
    def on_enter(self):
        app = App.get_running_app()
        self.rol = getattr(app, 'rol_actual', 2)
        usuario = app.usuario_actual
        es_nuevo = getattr(app, 'es_nuevo', False)

        if not getattr(app, 'bienvenida_mostrada', False):
            # Mensaje e ícono según rol o estado
            if es_nuevo:
                mensaje = f"¡Hola {usuario}, gracias por registrarte!"
                icon_name = "star"
                icon_color = (1, 0.8, 0.2, 1)
            elif self.rol == 1:
                mensaje = f"Bienvenido, {usuario} (Admin)"
                icon_name = "account-cog"
                icon_color = (1, 0.6, 0.2, 1)
            else:
                mensaje = f"Bienvenido de nuevo, {usuario}"
                icon_name = "account"
                icon_color = (0.6, 0.8, 1, 1)

            # Construcción del popup personalizado
            content = MDCard(
                orientation="vertical",
                padding=dp(20),
                spacing=dp(15),
                size_hint=(None, None),
                size=(dp(280), dp(220)),
                md_bg_color=(0.2, 0.2, 0.2, 0.85), 
                radius=[20, 20, 20, 20]
            )

            icon = MDIcon(
                icon=icon_name,
                halign="center",
                theme_text_color="Custom",
                text_color=icon_color,
                font_size="48sp"
            )
            label = MDLabel(
                text=mensaje,
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_style="Body1"
            )
            btn = MDRaisedButton(
                text="OK",
                md_bg_color=(0.8, 0.1, 0.1, 1),
                pos_hint={"center_x": 0.5},
                on_release=lambda x: popup.dismiss()
            )

            content.add_widget(icon)
            content.add_widget(label)
            content.add_widget(btn)

            popup = ModalView(
                                size_hint=(None, None),
                                size=(dp(300), dp(250)),
                                background_color=(0, 0, 0, 0.7),  # Transparencia igual al otro popup
                                auto_dismiss=False
                            )
            popup.add_widget(content)
            popup.open()

            app.bienvenida_mostrada = True

    def cerrar_sesion(self):
        app = App.get_running_app()
        app.bienvenida_mostrada = False
        app.usuario_actual = None
        app.root.current = 'pantalla1'
