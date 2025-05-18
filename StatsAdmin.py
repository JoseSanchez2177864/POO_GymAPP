from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from ConBD import crear_conexion

from kivy.lang import Builder
Builder.load_file("StatsAdmin.kv")

class StatsAdminp(Screen):
    def on_enter(self, *args):
        self.load_users()

    def load_users(self):
        self.ids.label_container.clear_widgets()

        conexion = crear_conexion()
        cursor = conexion.cursor()
        consulta = """
        SELECT u.Id, u.Nombre, u.Apellidos, u.Nombre_Usuario, AVG(ur.RM_Calculado), COUNT(ur.Ejercicio)
        FROM Usuarios u
        LEFT JOIN Usuarios_RM ur ON u.Id = ur.Usuario
        GROUP BY u.Id, u.Nombre, u.Apellidos, u.Nombre_Usuario
        """
        cursor.execute(consulta)
        usuarios = cursor.fetchall()
        conexion.close()

        if not usuarios:
            self.ids.label_container.add_widget(Label(text="No hay usuarios registrados.", color=(1, 1, 1, 1), halign="left"))
        else:
            for usuario in usuarios:
                user_column = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(5))
                user_column.bind(minimum_height=user_column.setter('height'))

                # Helper para crear labels con alineación derecha
                def create_right_aligned_label(text):
                    lbl = Label(
                        text=text,
                        color=(1, 1, 1, 1),
                        size_hint_y=None,
                        height=dp(25),
                        halign='left',
                        valign='middle'
                    )
                    lbl.bind(size=lambda lbl, w: setattr(lbl, 'text_size', (lbl.width, None)))
                    return lbl

                user_column.add_widget(create_right_aligned_label(f"Nombre: {usuario[1]} {usuario[2]}"))
                user_column.add_widget(create_right_aligned_label(f"Usuario: {usuario[3]}"))
                user_column.add_widget(create_right_aligned_label(f"Promedio RM: {usuario[4] if usuario[4] is not None else 0:.2f}"))
                user_column.add_widget(create_right_aligned_label(f"Total Ejercicios: {usuario[5]}"))

                # Espacio extra
                user_column.add_widget(Widget(size_hint_y=None, height=dp(10)))

                # Botón centrado
                button_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
                btn_estadisticas = MDRaisedButton(
                    text="Ver Estadísticas",
                    size_hint=(None, None),
                    size=(150, 35),
                    pos_hint={"center_x": 0.5}
                )
                btn_estadisticas.bind(on_release=lambda x, u=usuario[0]: self.ver_estadisticas_usuario(u))
                button_box.add_widget(btn_estadisticas)
                user_column.add_widget(button_box)

                # Añadimos el user_column y luego el separador
                self.ids.label_container.add_widget(user_column)
                self.ids.label_container.add_widget(SimpleSeparator())

    def ver_estadisticas_usuario(self, usuario_id):
        app = App.get_running_app()
        app.usuario_actual_id = usuario_id  # guardamos el ID seleccionado en app
        statsp_screen = app.root.get_screen('pantalla6')
        statsp_screen.usuario_id = usuario_id
        statsp_screen.limpiar_campos()

        # Reseteamos usuario en Statsp para forzar carga de ese usuario:
        statsp_screen = app.root.get_screen('pantalla6')  # o el nombre correcto de la pantalla
        statsp_screen.usuario_id = usuario_id
        statsp_screen.ejercicio_seleccionado = ""
        statsp_screen.ids.campo_ejercicio.text = ""
        statsp_screen.ids.info_ultimo_entrenamiento.text = ""
        statsp_screen.ids.grafica_rm.source = ""

        # Supongamos que estás en statsadmin y quieres ir a Statsp
        app = App.get_running_app()
        statsp_screen = app.root.get_screen('pantalla6')  # obtienes la pantalla Statsp
        statsp_screen.rol = 1  # le dices que el rol es admin
        app.root.current = 'pantalla6'  # cambias a esa pantalla




class SimpleSeparator(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(1)
        with self.canvas:
            Color(0.6, 0.6, 0.6, 1)  # Gris claro
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class VerticalSpace(Widget):
    def __init__(self, height=dp(10), **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = height


class TestApp(App):
    def build(self):
        return StatsAdminp()

if __name__ == "__main__":
    TestApp().run()
