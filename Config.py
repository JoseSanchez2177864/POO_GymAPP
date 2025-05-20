from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from ConBD import crear_conexion

Builder.load_file("Config.kv")


class Configp(Screen):
    rol = NumericProperty(2)
    nombre = StringProperty()
    apellidos = StringProperty()
    nombreusuario = StringProperty()
    correo = StringProperty()

    def on_enter(Self):
        app = MDApp.get_running_app()
        if getattr(app, 'desde_login', False):
            app.desde_login = False



    def mostrar_popup_info(self):
# Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Texto indicativo arriba
        titulo_texto = "Modificar Información"
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
        self.input_nombre = MDTextField(
                                        hint_text='Nombre',
                                        text=self.nombre,
                                        mode='rectangle',
                                        )
        self.input_apellidos = MDTextField(hint_text='Apellidos',
                                        text=self.apellidos,
                                        mode='rectangle',
                                        )
        self.input_nombreusuario = MDTextField(hint_text='Nombre de Usuario',
                                        text=self.nombreusuario,
                                        mode='rectangle',
                                        )
        self.input_correo = MDTextField(hint_text='Correo',
                                        text=self.correo,
                                        mode='rectangle',
                                        )

        layout.add_widget(self.input_nombre)
        layout.add_widget(self.input_apellidos)
        layout.add_widget(self.input_nombreusuario)
        layout.add_widget(self.input_correo)

        layout.add_widget(Widget(size_hint_y=None, height=40))

        # Botones
        guardar_btn = MDRaisedButton(
            text='Modificar Usuario',
            size_hint=(0.4, None),
            height=45,
            md_bg_color="green"    )
        guardar_btn.bind(on_release=self.guardar_info_actualizada)

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


    def guardar_info_actualizada(self, instance):
        nuevo_nombre = self.input_nombre.text.strip()
        nuevo_apellidos = self.input_apellidos.text.strip()
        nuevo_usuario = self.input_nombreusuario.text.strip()
        nuevo_correo = self.input_correo.text.strip()

        if not (nuevo_nombre and nuevo_apellidos and nuevo_usuario and nuevo_correo):
            return

        conn = crear_conexion()
        cursor = conn.cursor()
        app = App.get_running_app()
        usuario_actual = app.usuario_actual

        try:
            cursor.execute("""
                UPDATE Usuarios
                SET Nombre = ?, Apellidos = ?, Nombre_Usuario = ?, Correo = ?
                WHERE Nombre_Usuario = ?
            """, (nuevo_nombre, nuevo_apellidos, nuevo_usuario, nuevo_correo, usuario_actual))
            conn.commit()
            self.nombre = nuevo_nombre
            self.apellidos = nuevo_apellidos
            self.nombreusuario = nuevo_usuario
            self.correo = nuevo_correo
            app.usuario_actual = nuevo_usuario
            self.popup.dismiss()
        except Exception as e:
            print(f'❌ Error: {str(e)}')
        finally:
            conn.close()
    def mostrar_popup_contrasena(self):
    # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Texto indicativo arriba
        titulo_texto = "Cambiar Contraseña"
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
        self.old_pass_input = MDTextField(
            hint_text="Contraseña actual",
            mode="rectangle",
            password=True
        )
        self.new_pass_input = MDTextField(
            hint_text="Nueva contraseña",
            mode="rectangle",
            password=True
        )
        self.confirm_pass_input = MDTextField(
            hint_text="Confirmar nueva contraseña",
            mode="rectangle",
            password=True
        )

        layout.add_widget(self.old_pass_input)
        layout.add_widget(self.new_pass_input)
        layout.add_widget(self.confirm_pass_input)

        # Botones
        
        guardar_btn = MDRaisedButton(
                text='Guardar Cambios',
                size_hint=(0.4, None),
                height=45,
                md_bg_color="blue"
            )
        guardar_btn.bind(on_release=self.cambiar_contrasena)
        

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


    def cambiar_contrasena(self, instance):
        old_pass = self.old_pass_input.text
        new_pass = self.new_pass_input.text
        confirm_pass = self.confirm_pass_input.text

        if new_pass != confirm_pass:
            print('❌ Las contraseñas no coinciden')
            return

        conn = crear_conexion()
        cursor = conn.cursor()
        app = App.get_running_app()
        usuario = app.usuario_actual

        cursor.execute("SELECT Contraseña FROM Usuarios WHERE Nombre_Usuario = ?", (usuario,))
        actual = cursor.fetchone()

        if actual and actual[0] == old_pass:
            cursor.execute("UPDATE Usuarios SET Contraseña = ? WHERE Nombre_Usuario = ?", (new_pass, usuario))
            conn.commit()
            conn.close()
            self.popup.dismiss()
        else:
            print('❌ Contraseña actual incorrecta')

    def on_enter(self):
        self.obtener_dato_bd()

    def obtener_dato_bd(self):
        conn = crear_conexion()
        cursor = conn.cursor()
        app = App.get_running_app()
        self.rol = getattr(app, 'rol_actual', 2)
        usuario = app.usuario_actual
        cursor.execute("""
            SELECT Nombre, Apellidos, Nombre_Usuario, Correo FROM Usuarios WHERE Nombre_Usuario = ?
        """, (usuario,))
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

    def redirigir_por_rol(self):
        if self.rol == 1:
            self.manager.current = 'pantalla8'
        elif self.rol == 2:
            self.manager.current = 'pantalla9'

    def cerrar_sesion(self):
        app = App.get_running_app()
        # Limpiar las variables de sesión
        app.usuario_id = None
        app.usuario_actual = None
        app.rol_actual = None
        app.es_nuevo = False
        self.manager.current = "pantalla1" 
    
