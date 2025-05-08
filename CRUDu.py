from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
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
        consulta = """
        SELECT u.*, r.Descripcion 
        FROM Usuarios u
        LEFT JOIN Usuario_Rol ur ON u.Id = ur.Usuario
        LEFT JOIN Roles r ON ur.Rol = r.Id
        """
        cursor.execute(consulta)
        usuarios = cursor.fetchall()
        conexion.close()
        print("Usuarios: ", usuarios)
        
        if not usuarios:
            self.ids.label_container.add_widget(Label(text="No hay usuarios registrados.", color=(1, 1, 1, 1)))
        else:
            for usuario in usuarios:
                # Contenedor principal (Horizontal)
                user_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, padding=10, spacing=10)
                
                # Contenedor de información (Vertical)
                info_box = BoxLayout(orientation='vertical', size_hint_x=1.5)
                for info in [f"",
                    f"Nombre: {usuario[1]} {usuario[2]}     Nombre de Usuario: {usuario[7]}",
                    f"Correo: {usuario[3]}",
                    f"Plan: {usuario[6]}     Rol: {usuario[-1] if usuario[-1] else 'Sin Rol'}"
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
                    label.bind(texture_size=lambda inst, val: setattr(inst, 'height', inst.texture_size[1] + 10))
                    info_box.add_widget(label)
                
                # Contenedor de botones (Vertical)
                button_box = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=5, padding=(10,10))
                
                # Botón Cambiar Rol
                btn_editar = Button(text="Cambiar Rol", size_hint_y=None, height=30, size_hint_x=None, width=80)
                btn_editar.bind(on_release=lambda x, u=usuario: self.editar_usuario(u))
                
                # Botón Eliminar
                btn_eliminar = Button(text="Eliminar", size_hint_y=None, height=30, size_hint_x=None, width=80)
                btn_eliminar.bind(on_release=lambda x, u=usuario: self.eliminar_usuario(u))
                
                button_box.add_widget(btn_editar)
                button_box.add_widget(btn_eliminar)
                
                # Agregar las cajas al contenedor principal
                user_row.add_widget(info_box)
                user_row.add_widget(button_box)

                self.ids.label_container.add_widget(user_row)
    def actualizar_vista(self):
        self.load_users()

    # Métodos para manejar los botones (aún no implementados)
    def editar_usuario(self, usuario):
    # Obtener el rol actual del usuario
        rol_actual = usuario[-1]  # El rol está en la última posición de la tupla usuario

    # Determinar el nuevo rol (si es 'Administrador', cambiar a 'Usuario' y viceversa)
        nuevo_rol = 'Usuario' if rol_actual == 'Administrador' else 'Administrador'
    
    # Actualizar el rol en la base de datos
        conexion = crear_conexion()
        cursor = conexion.cursor()

    # Obtener el ID del rol (supongo que los roles tienen ID = 1 para Administrador y 2 para Usuario)
        cursor.execute("SELECT Id FROM Roles WHERE Descripcion = ?", (nuevo_rol,))
        nuevo_rol_id = cursor.fetchone()[0]

    # Actualizar el rol del usuario en la tabla Usuario_Rol
        cursor.execute("""
    UPDATE Usuario_Rol
    SET Rol = ?
    WHERE Usuario = ?
    """, (nuevo_rol_id, usuario[0]))
    
        conexion.commit()
        conexion.close()
    
        print(f"Rol del usuario {usuario[1]} {usuario[2]} cambiado a {nuevo_rol}.")
    
    # Actualizar la vista para reflejar el cambio
        self.actualizar_vista()


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

    def confirmar_eliminar_usuario(self, usuario, popup):
        # Eliminar el usuario de la base de datos
        conexion = crear_conexion()
        cursor = conexion.cursor()
    
        cursor.execute("DELETE FROM Usuarios WHERE Id = ?", (usuario[0],))
        cursor.execute("DELETE FROM Usuario_Rol WHERE Usuario = ?", (usuario[0],))
        conexion.commit()
        conexion.close()
    
        popup.dismiss()
        print(f"Usuario {usuario} eliminado.")
        self.actualizar_vista()  # Método para actualizar la vista de usuarios

class TestApp(App):
    def build(self):
        return CRUDup()

if __name__ == "__main__":
    TestApp().run()
