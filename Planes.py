from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.lang import Builder
from ConBD import crear_conexion

Builder.load_file("Planes.kv")

class Planesp(Screen):
    rol = NumericProperty(2)

    def on_enter(self, *args):
        self.load_users()  # Puedes cambiarlo a self.load_planes() si ajustas el nombre

    def load_users(self):
        self.ids.planes_container.clear_widgets()
        conexion = crear_conexion()
        cursor = conexion.cursor()
        consulta = "SELECT * FROM Planes"
        cursor.execute(consulta)
        planes = cursor.fetchall()
        conexion.close()
        
        if not planes:
            self.ids.planes_container.add_widget(
                Label(text="No hay planes registrados.", color=(1, 1, 1, 1))
            )
        else:
            for plan in planes:
                user_row = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=5)
                
                for info in [
                    f"ID: {plan[0]}",
                    f"Nombre: {plan[1]}",
                    f"Descripción: {plan[2]}",
                    f"Costo: ${plan[3]}"
                ]:
                    label = Label(
                        text=info,
                        size_hint_y=None,
                        height=30,
                        color=(1, 1, 1, 1),
                        halign='left',
                        valign='middle'
                    )
                    user_row.add_widget(label)

                self.ids.planes_container.add_widget(user_row)
