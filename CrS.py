from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from ConBD import crear_conexion

class CrSp(Screen):
    def mostrar_mensaje(self, titulo, mensaje):
        popup = Popup(
            title=titulo,
            content=Label(text=mensaje),
            size_hint=(None, None), 
            size=(400, 200),
            auto_dismiss=True
        )
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
                INSERT INTO Usuarios (Nombre, Apellidos, Nombre_Usuario, Correo, Contraseña, Peso, Planes)
                OUTPUT INSERTED.Id
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nombre, apellidos, nombre_usuario, correo, contrasena, peso, plan_por_defecto))

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
            App.get_running_app().usuario_actual = nombre_usuario
            App.get_running_app().es_nuevo = True
            self.manager.current = "pantalla3"

        except Exception as e:
            conn.rollback()
            print("❌ Error al crear el usuario:", e)
            self.mostrar_mensaje("Error", "No se pudo crear el usuario. Intenta nuevamente.")
        finally:
            conn.close()
