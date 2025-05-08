from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from ConBD import crear_conexion

# Cargamos el KV
Builder.load_file("Config.kv")

# Definimos la clase Configp
class Configp(Screen):
    rol = NumericProperty(2)
    nombre = StringProperty()
    apellidos = StringProperty()
    nombreusuario = StringProperty()
    correo = StringProperty()

    def mostrar_popup_info(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.input_nombre = TextInput(hint_text='Nombre', text=self.nombre)
        self.input_apellidos = TextInput(hint_text='Apellidos', text=self.apellidos)
        self.input_nombreusuario = TextInput(hint_text='Nombre de Usuario', text=self.nombreusuario)
        self.input_correo = TextInput(hint_text='Correo', text=self.correo)

        guardar_btn = Button(text='Guardar cambios', size_hint_y=None, height=40)
        guardar_btn.bind(on_release=self.guardar_info_actualizada)

        layout.add_widget(Label(text='Editar Información'))
        layout.add_widget(self.input_nombre)
        layout.add_widget(self.input_apellidos)
        layout.add_widget(self.input_nombreusuario)
        layout.add_widget(self.input_correo)
        layout.add_widget(guardar_btn)

        self.popup = Popup(title='Actualizar información',
                       content=layout,
                       size_hint=(None, None), size=(400, 500),
                       auto_dismiss=True)
        self.popup.open()

    def guardar_info_actualizada(self, instance):
        nuevo_nombre = self.input_nombre.text.strip()
        nuevo_apellidos = self.input_apellidos.text.strip()
        nuevo_usuario = self.input_nombreusuario.text.strip()
        nuevo_correo = self.input_correo.text.strip()

        if not (nuevo_nombre and nuevo_apellidos and nuevo_usuario and nuevo_correo):
            self.popup.content.add_widget(Label(text='❌ Todos los campos deben estar completos'))
            return

        conn = crear_conexion()
        cursor = conn.cursor()
        app = App.get_running_app()
        usuario_actual = app.usuario_actual

        try:
            cursor.execute("""
                UPDATE Usuarios
                SET Nombre = ?, Apellidos = ?, NombreUsuario = ?, Correo = ?
                WHERE NombreUsuario = ?
            """, (nuevo_nombre, nuevo_apellidos, nuevo_usuario, nuevo_correo, usuario_actual))
            conn.commit()            
            self.nombre = nuevo_nombre
            self.apellidos = nuevo_apellidos
            self.nombreusuario = nuevo_usuario
            self.correo = nuevo_correo
            app.usuario_actual = nuevo_usuario
            self.popup.dismiss()
        except Exception as e:
            self.popup.content.add_widget(Label(text=f'❌ Error: {str(e)}'))
        finally:
            conn.close()


    def mostrar_popup_contrasena(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.old_pass_input = TextInput(hint_text='Contraseña actual', password=True)
        self.new_pass_input = TextInput(hint_text='Nueva contraseña', password=True)
        self.confirm_pass_input = TextInput(hint_text='Confirmar nueva contraseña', password=True)

        cambiar_btn = Button(text='Cambiar contraseña', size_hint_y=None, height=40)
        cambiar_btn.bind(on_release=self.cambiar_contrasena)

        layout.add_widget(Label(text='Modificar Contraseña'))
        layout.add_widget(self.old_pass_input)
        layout.add_widget(self.new_pass_input)
        layout.add_widget(self.confirm_pass_input)
        layout.add_widget(cambiar_btn)

        self.popup = Popup(title='Cambiar contraseña',
                           content=layout,
                           size_hint=(None, None), size=(400, 400),
                           auto_dismiss=True)
        self.popup.open()

    def cambiar_contrasena(self, instance):
        old_pass = self.old_pass_input.text
        new_pass = self.new_pass_input.text
        confirm_pass = self.confirm_pass_input.text

        if new_pass != confirm_pass:
            self.popup.content.add_widget(Label(text='❌ Las contraseñas no coinciden'))
            return

        conn = crear_conexion()
        cursor = conn.cursor()
        app = App.get_running_app()
        usuario = app.usuario_actual

        cursor.execute("SELECT Contrasena FROM Usuarios WHERE NombreUsuario = ?", (usuario,))
        actual = cursor.fetchone()

        if actual and actual[0] == old_pass:
            cursor.execute("UPDATE Usuarios SET Contrasena = ? WHERE NombreUsuario = ?", (new_pass, usuario))
            conn.commit()
            conn.close()
            self.popup.dismiss()
        else:
            self.popup.content.add_widget(Label(text='❌ Contraseña actual incorrecta'))

    def on_enter(self):
        self.obtener_dato_bd()
        app = App.get_running_app()
    def obtener_dato_bd(self):
        conn = crear_conexion()
        cursor = conn.cursor()
        app = App.get_running_app()
        self.rol = getattr(app, 'rol_actual', 2)
        app = App.get_running_app()
        usuario = app.usuario_actual
        # Asegúrate de que los nombres de columnas sean correctos y no tengan espacios
        cursor.execute(
        "SELECT Nombre, Apellidos, NombreUsuario, Correo FROM Usuarios WHERE NombreUsuario = ?",
        (usuario,)
    )
        dato = cursor.fetchone()

        conn.close()

        if dato:
            self.nombre = dato[0]
            self.apellidos = dato[1]
            self.nombreusuario = dato[2]
            self.correo = dato[3]
        else:
            self.nombre = "No encontrado"
            self.apellidos = ""
            self.nombreusuario = ""
            self.correo = ""