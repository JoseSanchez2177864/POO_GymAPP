from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivy.uix.modalview import ModalView
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from ConBD import crear_conexion

Builder.load_file("CRUDp.kv")

class CRUDpp(Screen):
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        if getattr(app, 'desde_login', False):
            app.desde_login = False
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
                btn_editar.bind(on_release=lambda x, u=plan: self.mostrar_popup_plan(modificar=True, plan=u))

                btn_eliminar = MDRaisedButton(text="Eliminar", size_hint=(None, None), size=(110, 35))
                btn_eliminar.bind(on_release=lambda x, u=plan: self.eliminar_usuario(u))

                button_box.add_widget(btn_editar)
                button_box.add_widget(btn_eliminar)

                user_column.add_widget(button_box)

                self.ids.label_container.add_widget(user_column)

    def actualizar_vista(self):
        self.load_users()

    def mostrar_popup_agregar(self):
        self.mostrar_popup_plan(modificar=False)

    def mostrar_popup_plan(self, modificar=False, plan=None):
    # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Texto indicativo arriba
        titulo_texto = "Modificar Plan" if modificar else "Agregar Plan"
        titulo = Label(
            text=titulo_texto,
            size_hint_y=None,
            height=30,
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True,
            halign='center'
        )
        # Para que el texto se centre correctamente
        titulo.bind(size=lambda s, w: setattr(s, 'text_size', w))

        layout.add_widget(titulo)

        # Inputs
        self.nombre_plan_input = MDTextField(
            hint_text="Nombre del plan",
            mode="rectangle",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            text=plan[1] if modificar and plan else ""
        )
        self.descripcion_plan_input = MDTextField(
            hint_text="Descripción del plan",
            mode="rectangle",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            multiline=True,
            text=plan[2] if modificar and plan else ""
        )
        self.costo_plan_input = MDTextField(
            hint_text="Costo del plan",
            mode="rectangle",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            input_filter="float",
            text=str(plan[3]) if modificar and plan else ""
        )

        layout.add_widget(self.nombre_plan_input)
        layout.add_widget(self.descripcion_plan_input)
        layout.add_widget(self.costo_plan_input)

        # Botones
        if modificar:
            guardar_btn = MDRaisedButton(
                text='Guardar Cambios',
                size_hint=(0.4, None),
                height=45,
                md_bg_color="blue"
            )
            guardar_btn.bind(on_release=lambda x: self.guardar_info_actualizada(plan[0]))
        else:
            guardar_btn = MDRaisedButton(
                text='Agregar Plan',
                size_hint=(0.4, None),
                height=45,
                md_bg_color="green"
            )
            guardar_btn.bind(on_release=self.agregar_plan)

        cancelar_btn = MDFlatButton(
            text='Cancelar',
            size_hint=(0.4, None),
            height=45,
            text_color="red"
        )
        cancelar_btn.bind(on_release=lambda x: self.popup.dismiss())

        button_box = BoxLayout(orientation='horizontal', spacing=20, padding=[0, 10])
        button_box.add_widget(cancelar_btn)
        button_box.add_widget(guardar_btn)

        layout.add_widget(button_box)

        # Crear y abrir popup
        self.popup = ModalView(
            size_hint=(0.9, None),
            height=480,  # un poco más alto para el título
            auto_dismiss=False,
            background_color=(0, 0, 0, 0.7)
        )
        self.popup.add_widget(layout)
        self.popup.open()

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

        self.popup.dismiss()
        print(f"Plan '{nombre}' agregado correctamente.")
        self.actualizar_vista()

    def guardar_info_actualizada(self, plan_id):
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
            UPDATE Planes SET Nombre = ?, Descripcion = ?, Costo = ? WHERE Id = ?
        """, (nombre, descripcion, costo, plan_id))

        conexion.commit()
        conexion.close()

        self.popup.dismiss()
        print(f"Plan '{nombre}' modificado correctamente.")
        self.actualizar_vista()

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
