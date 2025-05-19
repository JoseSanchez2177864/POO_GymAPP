from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
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
        app = MDApp.get_running_app()
        if getattr(app, 'desde_login', False):
            app.desde_login = False 

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
                # Contenedor principal vertical para texto y botones
                user_column = BoxLayout(orientation='vertical', size_hint_y=None, padding=10, spacing=10)
                user_column.bind(minimum_height=user_column.setter('height'))
                
                # Contenedor info vertical
                info_box = BoxLayout(orientation='vertical', size_hint_y=None)
                info_box.bind(minimum_height=info_box.setter('height'))
                
                lines = [
                    f"Nombre: {usuario[1]} {usuario[2]}     Nombre de Usuario: {usuario[3]}",
                    f"Correo: {usuario[4]}",
                    f"Plan: {usuario[8]}     Rol: {usuario[-1] if usuario[-1] else 'Sin Rol'}"
                ]

                for i, info in enumerate(lines):
                    if i == 0:
                        label = Label(
                            text=info,
                            size_hint_y=None,
                            color=(1, 1, 1, 1),
                            text_size=(self.ids.label_container.width - 40, None),
                            halign='left',
                            valign='top'
                        )
                        label.bind(texture_size=lambda inst, val: setattr(inst, 'height', inst.texture_size[1] + 10))
                    else:
                        label = Label(
                            text=info,
                            size_hint_y=None,
                            height=30,
                            color=(1, 1, 1, 1),
                            text_size=(self.ids.label_container.width - 40, None),
                            halign='left',
                            valign='middle'
                        )
                        label.bind(texture_size=lambda inst, val: setattr(inst, 'height', inst.texture_size[1] + 5))
                    info_box.add_widget(label)
                
                user_column.add_widget(info_box)

                # Espacio entre texto y botones
                user_column.add_widget(Widget(size_hint_y=None, height=10))
                
                # Contenedor botones horizontal, centrados
                button_box = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=40)
                
                btn_editar = MDRaisedButton(
                    text="Cambiar Rol",
                    size_hint=(None, None),
                    size=(110, 35),
                    pos_hint={"center_x": 0.5}
                )
                btn_editar.bind(on_release=lambda x, u=usuario: self.editar_usuario(u))
                
                btn_eliminar = MDRaisedButton(
                    text="Eliminar",
                    size_hint=(None, None),
                    size=(110, 35),
                    pos_hint={"center_x": 0.5}
                )
                btn_eliminar.bind(on_release=lambda x, u=usuario: self.eliminar_usuario(u))
                
                button_box.add_widget(btn_editar)
                button_box.add_widget(btn_eliminar)
                
                user_column.add_widget(button_box)

                # Espacio debajo de los botones
                user_column.add_widget(Widget(size_hint_y=None, height=15))
                
                self.ids.label_container.add_widget(user_column)

    def actualizar_vista(self):
        self.load_users()

    def editar_usuario(self, usuario):
        rol_actual = usuario[-1]
        nuevo_rol = 'Usuario' if rol_actual == 'Administrador' else 'Administrador'

        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT Id FROM Roles WHERE Descripcion = ?", (nuevo_rol,))
        nuevo_rol_id = cursor.fetchone()[0]

        cursor.execute("""
        UPDATE Usuario_Rol
        SET Rol = ?
        WHERE Usuario = ?
        """, (nuevo_rol_id, usuario[0]))

        conexion.commit()
        conexion.close()

        print(f"Rol del usuario {usuario[1]} {usuario[2]} cambiado a {nuevo_rol}.")
        self.actualizar_vista()

    def eliminar_usuario(self, usuario):
        texto = f"¿Estás seguro de que deseas eliminar a {usuario[1]}?"
        
        btn_si = MDFlatButton(text="Sí", on_release=lambda x: self.confirmar_eliminar_usuario(usuario, self.dialog))
        btn_no = MDFlatButton(text="No", on_release=lambda x: self.dialog.dismiss())
        
        self.dialog = MDDialog(
            title="Confirmar Eliminación",
            text=texto,
            buttons=[btn_si, btn_no],
            auto_dismiss=False
        )
        self.dialog.open()

    def confirmar_eliminar_usuario(self, usuario, dialog):
        conexion = crear_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM Usuarios WHERE Id = ?", (usuario[0],))
        cursor.execute("DELETE FROM Usuario_Rol WHERE Usuario = ?", (usuario[0],))
        conexion.commit()
        conexion.close()

        dialog.dismiss()
        print(f"Usuario {usuario} eliminado.")
        self.actualizar_vista()

class TestApp(App):
    def build(self):
        return CRUDup()

if __name__ == "__main__":
    TestApp().run()