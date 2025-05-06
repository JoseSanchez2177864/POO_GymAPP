# app.py
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from ConBD import crear_conexion

# Cargamos el KV
Builder.load_file("CrS.kv")

# Definimos la primera pantalla
class CrSp(Screen):
    def mostrar_mensaje(self, titulo, mensaje):
        popup = Popup(title=titulo,
                  content=Label(text=mensaje),
                  size_hint=(None, None), size=(400, 200))
        popup.open()
    def crear_usuario(self):
        nombre_usuario = self.ids.nombreusuario_input.text
        nombre = self.ids.nombre_input.text
        apellidos = self.ids.apellidos_input.text
        correo = self.ids.correo_input.text
        contrasena = self.ids.contrasena_input.text
        plan_por_defecto = 1
        rol_por_defecto = 2

        try:
            peso = float(self.ids.peso_input.text)
        except ValueError:
            self.mostrar_mensaje("Peso Inválido", "El peso incial del usuario ya no es válido. Inserte una cifra")
            print("❌ Peso no válido.")
            return

        conn = crear_conexion()
        cursor = conn.cursor()

        try:
        # Verificar si el nombre de usuario o el correo ya existen
            cursor.execute("""
                SELECT NombreUsuario, Correo FROM usuarios 
                WHERE NombreUsuario = ? OR Correo = ?
            """, (nombre_usuario, correo))

            resultado = cursor.fetchone()
            if resultado:
                if resultado[0] == nombre_usuario and resultado[1] == correo:
                    self.mostrar_mensaje("Datos en uso", "El nombre de usuario y el correo ya están en uso.")
                elif resultado[0] == nombre_usuario:
                    self.mostrar_mensaje("Nombre de usuario", "El nombre de usuario ya está en uso.")
                else:
                    self.mostrar_mensaje("Correo", "El correo ya está en uso.")
                return


        # Insertar usuario
            cursor.execute("""
            INSERT INTO usuarios (Nombre, Apellidos, Correo, Contrasena, Peso, Planes, NombreUsuario)
            OUTPUT INSERTED.Id
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, apellidos, correo, contrasena, peso, plan_por_defecto, nombre_usuario))

            usuario_id = cursor.fetchone()[0]
            print(f"✅ Usuario insertado con ID: {usuario_id}")

        # Insertar rol
            cursor.execute("INSERT INTO Usuario_Rol (Usuario, Rol) VALUES (?, ?)", (usuario_id, rol_por_defecto))

            conn.commit()
            print("✅ Usuario y rol registrados correctamente.")

# Justo después de insertar el usuario y antes de cambiar de pantalla
            App.get_running_app().usuario_actual = nombre_usuario
            App.get_running_app().es_nuevo = True  # Marcar que es recién creado
            self.manager.current = "pantalla3"
        except Exception as e:
            print("❌ Error al crear el usuario:", e)
            conn.rollback()
        finally:
            conn.close()


