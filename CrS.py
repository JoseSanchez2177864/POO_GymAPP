from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.uix.modalview import ModalView
from ConBD import crear_conexion

class CrSp(Screen):
    def mostrar_mensaje(self, titulo, mensaje):
        # Layout principal del popup
        layout = BoxLayout(orientation="vertical", spacing=15, padding=20)

        # Título estilizado
        titulo_label = MDLabel(
            text=titulo,
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 0.3, 0.3, 1),
            bold=True,
            font_style="H6"
        )

        # Mensaje
        mensaje_label = MDLabel(
            text=mensaje,
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.9),
        )

        # Botón cerrar
        cerrar_btn = MDRaisedButton(
            text="Cerrar",
            md_bg_color=(0.8, 0.1, 0.1, 1),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: popup.dismiss()
        )

        layout.add_widget(titulo_label)
        layout.add_widget(mensaje_label)
        layout.add_widget(Widget(size_hint_y=None, height=10))
        layout.add_widget(cerrar_btn)

        # Contenedor visual
        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint=(None, None),
            size=(dp(280), dp(200)),
            md_bg_color=(0.2, 0.2, 0.2, 0.85),
            radius=[20, 20, 20, 20]
        )
        card.add_widget(layout)

        # ModalView con transparencia
        popup = ModalView(
            size_hint=(None, None),
            size=(dp(300), dp(220)),
            background_color=(0, 0, 0, 0.7),
            auto_dismiss=True
        )
        popup.add_widget(card)
        popup.open()

    def crear_usuario(self):
        nombre_usuario = self.ids.nombreusuario_input.text.strip()
        nombre = self.ids.nombre_input.text.strip()
        apellidos = self.ids.apellidos_input.text.strip()
        correo = self.ids.correo_input.text.strip()
        contrasena = self.ids.contrasena_input.text.strip()
        plan_por_defecto = 1
        rol_por_defecto = 2

        # Validación de campos vacíos
        if not nombre_usuario or not nombre or not apellidos or not correo or not contrasena:
            self.mostrar_mensaje("Campos Vacíos", "Por favor, completa todos los campos obligatorios.")
            return

        try:
            peso = float(self.ids.peso_input.text)
        except (ValueError, AttributeError):
            peso = None  # NULL en la DB

        conn = crear_conexion()
        cursor = conn.cursor()

        try:
            # Validar usuario o correo duplicado
            cursor.execute("""
                SELECT 1 FROM Usuarios WHERE Nombre_Usuario = ? OR Correo = ?
            """, (nombre_usuario, correo))
            if cursor.fetchone():
                self.mostrar_mensaje("Datos en uso", "El nombre de usuario o el correo ya están en uso.")
                return

            # Insertar usuario con OUTPUT para obtener Id insertado
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Apellidos, Nombre_Usuario, Correo, Contraseña, Peso)
                OUTPUT INSERTED.Id
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, apellidos, nombre_usuario, correo, contrasena, peso))

            usuario_id = cursor.fetchone()
            if usuario_id is None:
                raise Exception("No se pudo obtener el ID del usuario.")

            usuario_id = usuario_id[0]

            # Insertar rol para el usuario
            cursor.execute("""
                INSERT INTO Usuario_Rol (Usuario, Rol)
                VALUES (?, ?)
            """, (usuario_id, rol_por_defecto))

            conn.commit()
            print(f"✅ Usuario (ID: {usuario_id}) y rol registrados correctamente.")

            # Guardar el usuario creado en la app para sesión
            app = App.get_running_app()
            app.usuario_id = usuario_id       # Guardar ID del usuario
            app.usuario_actual = nombre_usuario
            app.rol_actual = rol_por_defecto
            app.es_nuevo = True
            self.manager.current = "pantalla3"

        except Exception as e:
            conn.rollback()
            print("❌ Error al crear el usuario:", e)
            self.mostrar_mensaje("Error", "No se pudo crear el usuario. Intenta nuevamente.")
        finally:
            conn.close()
