from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
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
            self.ids.label_container.add_widget(Label(text="No hay usuarios registrados.", color=(1, 1, 1, 1)))
        else:
            for plan in planes:
                user_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, padding=10, spacing=10)
                
                info_box = BoxLayout(orientation='vertical', size_hint_x=1.5)
                for info in [
                    f"ID: {plan[0]}",
                    f"Nombre: {plan[1]}",
                    f"Descripción: {plan[2]}",
                    f"Costo: ${plan[3]}"
                ]:
                    label = Label(
                        text=info,
                        size_hint_y=None,
                        height=40,
                        color=(1, 1, 1, 1),
                        text_size=(self.width - 200, None),
                        halign='left',
                        valign='middle'
                    )
                    info_box.add_widget(label)
                
                button_box = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=5, padding=(10,10))
                
                btn_editar = Button(text="Modificar Plan", size_hint_y=None, height=30)
                btn_editar.bind(on_release=lambda x, u=plan[0]: self.mostrar_popup_info(u))
                
                btn_eliminar = Button(text="Eliminar", size_hint_y=None, height=30)
                btn_eliminar.bind(on_release=lambda x, u=plan: self.eliminar_usuario(u))
                
                button_box.add_widget(btn_editar)
                button_box.add_widget(btn_eliminar)
                
                user_row.add_widget(info_box)
                user_row.add_widget(button_box)
                self.ids.label_container.add_widget(user_row)

    def actualizar_vista(self):
        self.load_users()

    def eliminar_usuario(self, usuario):
        print(f"Eliminar usuario: {usuario[0]}")
        # Confirmación de eliminación
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text=f"¿Estás seguro de que deseas eliminar a {usuario[1]}?")
        layout.add_widget(label)
    
        botones = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_si = Button(text="Sí")
        btn_no = Button(text="No")

        popup = Popup(title="Confirmar Eliminación", content=layout, size_hint=(0.5, 0.3))

        btn_si.bind(on_release=lambda x: self.confirmar_eliminar_usuario(usuario, popup))
        btn_no.bind(on_release=popup.dismiss)

        botones.add_widget(btn_si)
        botones.add_widget(btn_no)
        layout.add_widget(botones)

        popup.open()

    def confirmar_eliminar_usuario(self, planes, popup):
        # Eliminar el usuario de la base de datos
        conexion = crear_conexion()
        cursor = conexion.cursor()
    
        cursor.execute("DELETE FROM Planes WHERE Id = ?", (planes[0],))
        cursor.execute("UPDATE Usuarios SET Planes = 1 WHERE Planes = ?", (planes[0],))
        conexion.commit()
        conexion.close()
    
        popup.dismiss()
        print(f"Usuario {planes} eliminado.")
        self.actualizar_vista()  # Método para actualizar la vista de usuarios

    def mostrar_popup_info(self, plan_id):
        self.obtener_dato_bd(plan_id)  # Obtener los datos del plan

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.input_nombre = TextInput(hint_text='Nombre', text=self.nombre_plan)
        self.input_descripcion = TextInput(hint_text='Descripción', text=self.descripcion)
        self.input_costo = TextInput(hint_text='Costo', text=str(self.costo))
        
        guardar_btn = Button(text='Guardar cambios', size_hint_y=None, height=40)
        guardar_btn.bind(on_release=lambda x: self.guardar_info_actualizada(plan_id))

        layout.add_widget(Label(text='Editar Información'))
        layout.add_widget(self.input_nombre)
        layout.add_widget(self.input_descripcion)
        layout.add_widget(self.input_costo)
        layout.add_widget(guardar_btn)

        self.popup = Popup(title='Actualizar información',
                        content=layout,
                        size_hint=(None, None), size=(400, 500),
                        auto_dismiss=True)
        self.popup.open()

    def obtener_dato_bd(self, plan_id):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre, Descripcion, Costo FROM Planes WHERE Id = ?", (plan_id,))
        dato = cursor.fetchone()
        conn.close()

        if dato:
            self.nombre_plan = dato[0]
            self.descripcion = dato[1]
            self.costo = dato[2]
        else:
            self.nombre_plan = ""
            self.descripcion = ""
            self.costo = 0

    def guardar_info_actualizada(self, plan_id):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Planes 
            SET Nombre = ?, Descripcion = ?, Costo = ? 
            WHERE Id = ?
        """, (self.input_nombre.text, self.input_descripcion.text, float(self.input_costo.text), plan_id))
        conn.commit()
        conn.close()
        self.popup.dismiss()
        print(f"Plan {plan_id} actualizado correctamente.")
        self.actualizar_vista()

    def mostrar_popup_agregar(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.nombre_plan_input = TextInput(hint_text="Nombre para identificar el plan")
        self.descripcion_plan_input = TextInput(hint_text="Descripción del plan")
        self.costo_plan_input = TextInput(hint_text="Precio del plan $0.00")
        
        guardar_btn = Button(text='Agregar Plan', size_hint_y=None, height=40)
        guardar_btn.bind(on_release=self.agregar_plan)

        layout.add_widget(Label(text='Agregar Nuevo Plan'))
        layout.add_widget(self.nombre_plan_input)
        layout.add_widget(self.descripcion_plan_input)
        layout.add_widget(self.costo_plan_input)
        layout.add_widget(guardar_btn)

        self.popup = Popup(title='Agregar Plan',
                        content=layout,
                        size_hint=(None, None), size=(400, 500),
                        auto_dismiss=True)
        self.popup.open()

    def agregar_plan(self, *args):
        nombre_plan = self.nombre_plan_input.text
        descripcion_plan = self.descripcion_plan_input.text
        costo_plan = self.costo_plan_input.text
        if not nombre_plan or not descripcion_plan or not costo_plan:
            print("Todos los campos son obligatorios.")
            return

        try:
            costo = float(costo_plan)  # Convertir el costo a número
        except ValueError:
            print("El costo debe ser un valor numérico.")
            return

        # Conectar a la base de datos y agregar el nuevo plan
        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO Planes (Nombre, Descripcion, Costo)
            VALUES (?, ?, ?)
        """, (nombre_plan, descripcion_plan, costo))

        conexion.commit()
        conexion.close()

        # Cerrar el popup
        self.popup.dismiss()
        print(f"Plan '{nombre_plan}' agregado exitosamente.")

        # Actualizar la vista para mostrar el nuevo plan
        self.actualizar_vista()

