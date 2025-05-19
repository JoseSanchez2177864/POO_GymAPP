from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDLabel, MDIcon
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from ConBD import crear_conexion

from kivy.lang import Builder
Builder.load_file("Planes.kv")


class Planesp(Screen):
    rol = 2  # ejemplo, cambia según tu lógica
    def on_enter(self, *args):
        self.load_planes()
        app = MDApp.get_running_app()
        if getattr(app, 'desde_login', False):
            app.desde_login = False 

    def load_planes(self):
        self.ids.planes_container.clear_widgets()
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Planes")
        planes = cursor.fetchall()
        conexion.close()

        if not planes:
            self.ids.planes_container.add_widget(
                Label(text="No hay planes registrados.", color=(1, 1, 1, 1))
            )
        else:
            for plan in planes:
                plan_box = BoxLayout(orientation='vertical', size_hint_y=None, height=180, padding=5, spacing=5)

                # Mostrar información del plan
                for info in [
                    f"ID: {plan[0]}",
                    f"Nombre: {plan[1]}",
                    f"Descripción: {plan[2]}",
                    f"Costo: ${plan[3]}"
                ]:
                    label = Label(
                        text=info,
                        size_hint_y=None,
                        height=25,
                        color=(1, 1, 1, 1),
                        halign='left',
                        valign='middle'
                    )
                    label.bind(size=lambda s, w: setattr(s, 'text_size', w))
                    plan_box.add_widget(label)

                # Botón Comprar
                btn_comprar = MDRaisedButton(
                    text="Comprar",
                    size_hint_y=None,
                    height=40,
                    md_bg_color=(0.1, 0.6, 0.1, 1)
                )
                btn_comprar.bind(on_release=lambda btn, p=plan: self.mostrar_popup_compra(p))
                plan_box.add_widget(btn_comprar)

                self.ids.planes_container.add_widget(plan_box)

    def mostrar_popup_compra(self, plan):
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
            icon="cart",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.2, 1),
            font_size="48sp"
        )

        label = MDLabel(
            text=f"¿Deseas comprar el plan:\n{plan[1]} por ${plan[3]}?",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="Body1"
        )

        btn_ok = MDRaisedButton(
            text="Comprar",
            md_bg_color=(0.1, 0.6, 0.1, 1),
            pos_hint={"center_x": 0.5}
        )
        btn_cancel = MDRaisedButton(
            text="Cancelar",
            md_bg_color=(0.6, 0.1, 0.1, 1),
            pos_hint={"center_x": 0.5}
        )

        content.add_widget(icon)
        content.add_widget(label)
        content.add_widget(btn_ok)
        content.add_widget(btn_cancel)

        popup = ModalView(
            size_hint=(None, None),
            size=(dp(300), dp(280)),
            background_color=(0, 0, 0, 0.7),
            auto_dismiss=False
        )
        popup.add_widget(content)

        btn_ok.bind(on_release=lambda x: self._comprar_plan_confirmado(plan, popup))
        btn_cancel.bind(on_release=popup.dismiss)

        popup.open()

    def _comprar_plan_confirmado(self, plan, popup):
        usuario_id = self.obtener_usuario_id()
        if not usuario_id:
            print("No hay usuario logueado.")
            popup.dismiss()
            return

        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Usuarios SET Planes = ? WHERE Id = ?",
                (plan[0], usuario_id)
            )
            conn.commit()
            conn.close()
            print("Plan actualizado correctamente.")
        except Exception as e:
            print(f"Error actualizando plan: {e}")

        popup.dismiss()

    def obtener_usuario_id(self):
        # Obtiene el id del usuario logueado desde la app
        app = App.get_running_app()
        usuario_actual = getattr(app, 'usuario_actual', None)
        if not usuario_actual:
            return None

        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT Id FROM Usuarios WHERE Nombre_Usuario = ?", (usuario_actual,))
            resultado = cursor.fetchone()
            conn.close()
            if resultado:
                return resultado[0]
            return None
        except Exception as e:
            print(f"Error obteniendo id usuario: {e}")
            return None
