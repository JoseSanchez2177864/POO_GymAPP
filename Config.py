from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from ConBD import crear_conexion

# Cargamos el KV
Builder.load_file("Config.kv")

# Definimos la clase Configp
class Configp(Screen):
    # Creamos una propiedad para vincularla con el texto del Label
    db_data = StringProperty()

    def on_enter(self):
        # Al ingresar a la pantalla, obtenemos los datos de la base de datos
        self.db_data = self.obtener_dato_bd()

    def obtener_dato_bd(self):
        # Conectamos a la base de datos utilizando la función de tu módulo ConBD
        conn = crear_conexion()  # Ajusta esto a tu implementación de ConBD
        cursor = conn.cursor()

        # Realizamos una consulta a la base de datos (ajusta la consulta según tus necesidades)
        cursor.execute("SELECT dato FROM tabla WHERE id = 1")
        dato = cursor.fetchone()

        # Cerramos la conexión
        conn.close()

        # Si se obtiene un dato, lo devolvemos, de lo contrario, un mensaje por defecto
        if dato:
            return dato[0]  # Asumiendo que "dato" es un solo campo
        return "No se encontró dato"


