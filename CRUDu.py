from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder
from ConBD import crear_conexion

Builder.load_file("CRUDu.kv")

class CRUDup(Screen):
    def on_enter(self, *args):
        self.load_users()

    def load_users(self):
        self.ids.label_container.clear_widgets()

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Usuarios")
        usuarios = cursor.fetchall()
        conexion.close()
        print("Usuarios: ",usuarios)
        if not usuarios:
            self.ids.label_container.add_widget(Label(text="No hay usuarios registrados.", color=(1, 1, 1, 1)))
        else:
            for usuario in usuarios:
                user_box = BoxLayout(orientation='vertical', padding=10, spacing=5, size_hint_y=None)
                user_box.bind(minimum_height=user_box.setter('height'))

                # Fondo negro para evitar "rectángulo blanco"
                with user_box.canvas.before:
                    Color(0, 0, 0, 1)  # negro
                    rect = Rectangle(size=user_box.size, pos=user_box.pos)
                user_box.bind(size=lambda inst, val: setattr(rect, 'size', inst.size))
                user_box.bind(pos=lambda inst, val: setattr(rect, 'pos', inst.pos))

                for info in [f"Nombre: {usuario[1]}{usuario[2]}     Nombre de Usuario: {usuario[7]}", f"Correo: {usuario[3]}", f"Plan: {usuario[6]}"]:
                    label = Label(
                        text=info,
                        size_hint_y=None,
                        color=(1, 1, 1, 1),  # texto blanco
                        text_size=(self.width - 40, None),
                        halign='left',
                        valign='middle'
                    )

                    # Ajustar altura automáticamente según el texto
                    # Ajustar altura automáticamente según el texto
                    def update_height(inst, val):
                        inst.height = inst.texture_size[1] + 10
                    label.bind(texture_size=update_height)


                    user_box.add_widget(label)

                self.ids.label_container.add_widget(user_box)

class TestApp(App):
    def build(self):
        return CRUDup()

if __name__ == "__main__":
    TestApp().run()

