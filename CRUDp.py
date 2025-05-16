from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from ConBD import crear_conexion

Builder.load_file("CRUDp.kv")

class CRUDpp(Screen):
    def on_enter(self, *args):
        self.load_users()

    def load_users(self):
        self.ids.label_container.clear_widgets()
        conexion = crear_conexion()
        cursor = conexion.cursor()
        consulta = "SELECT * FROM Planes"
        cursor.execute(consulta)
        planes = cursor.fetchall()
        conexion.close()

        if not planes:
            self.ids.label_container.add_widget(Label(text="No hay planes registrados.", color=(1, 1, 1, 1)))
        else:
            for plan in planes:
                user_column = BoxLayout(orientation='vertical', size_hint_y=None, padding=[40,10,10,10], spacing=10)
                user_column.bind(minimum_height=user_column.setter('height'))

                lines = [
                    f"ID: {plan[0]}",
                    f"Nombre: {plan[1]}",
                    f"Descripción: {plan[2]}",
                    f"Costo: ${plan[3]}"
                ]

                for info in lines:
                    label = Label(
                        text=info,
                        size_hint_y=None,
                        color=(1, 1, 1, 1),
                        text_size=(self.width - 60, None),
                        halign='left',
                        valign='middle'
                    )
                    label.bind(texture_size=lambda inst, val: setattr(inst, 'height', inst.texture_size[1] + 5))
                    user_column.add_widget(label)

                button_box = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=40)

                btn_editar = MDRaisedButton(text="Modificar Plan", size_hint=(None, None), size=(110, 35))
                btn_editar.bind(on_release=lambda x, u=plan: self.mostrar_popup_info(u))

                btn_eliminar = MDRaisedButton(text="Eliminar", size_hint=(None, None), size=(110, 35))
                btn_eliminar.bind(on_release=lambda x, u=plan: self.eliminar_usuario(u))

                button_box.add_widget(btn_editar)
                button_box.add_widget(btn_eliminar)

                user_column.add_widget(button_box)

                self.ids.label_container.add_widget(user_column)

    def actualizar_vista(self):
        self.load_users()

    def mostrar_popup_agregar(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.nombre_plan_input = TextInput(hint_text="Nombre del plan")
        self.descripcion_plan_input = TextInput(hint_text="Descripción del plan")
        self.costo_plan_input = TextInput(hint_text="Costo del plan")

        guardar_btn = MDRaisedButton(text='Agregar Plan', size_hint_y=None, height=40)
        guardar_btn.bind(on_release=self.agregar_plan)

        layout.add_widget(self.nombre_plan_input)
        layout.add_widget(self.descripcion_plan_input)
        layout.add_widget(self.costo_plan_input)

        self.dialog = MDDialog(title='Agregar Plan', type='custom', content_cls=layout, size_hint=(0.5, 0.5))
        self.dialog.open()

    def agregar_plan(self, *args):
        nombre = self.nombre_plan_input.text
        descripcion = self.descripcion_plan_input.text
        costo = self.costo_plan_input.text

        if not nombre or not descripcion or not costo:
            print("Todos los campos son obligatorios.")
            return

        try:
            costo = float(costo)
        except ValueError:
            print("El costo debe ser numérico.")
            return

        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO Planes (Nombre, Descripcion, Costo)
            VALUES (?, ?, ?)
        """, (nombre, descripcion, costo))

        conexion.commit()
        conexion.close()

        self.dialog.dismiss()
        print(f"Plan '{nombre}' agregado correctamente.")
        self.actualizar_vista()

    def mostrar_popup_info(self, plan):
        self.obtener_dato_bd(plan[0])

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.input_nombre = TextInput(hint_text='Nombre', text=self.nombre_plan)
        self.input_descripcion = TextInput(hint_text='Descripción', text=self.descripcion)
        self.input_costo = TextInput(hint_text='Costo', text=str(self.costo))

        guardar_btn = MDRaisedButton(text='Guardar cambios')
        guardar_btn.bind(on_release=lambda x: self.guardar_info_actualizada(plan[0]))

        layout.add_widget(self.input_nombre)
        layout.add_widget(self.input_descripcion)
        layout.add_widget(self.input_costo)
        layout.add_widget(guardar_btn)

        self.dialog = MDDialog(title='Modificar Plan', type='custom', content_cls=layout, size_hint=(0.5, 0.5))
        self.dialog.open()

    def eliminar_usuario(self, plan):
        self.dialog = MDDialog(
            title="Confirmar Eliminación",
            text=f"¿Estás seguro de que deseas eliminar el plan '{plan[1]}'?",
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Eliminar", on_release=lambda x: self.confirmar_eliminar_usuario(plan))
            ]
        )
        self.dialog.open()

    def confirmar_eliminar_usuario(self, plan):
        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM Planes WHERE Id = ?", (plan[0],))
        conexion.commit()
        conexion.close()

        self.dialog.dismiss()
        print(f"Plan '{plan[1]}' eliminado correctamente.")
        self.actualizar_vista()
