import os
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from ConBD import crear_conexion
from kivy.lang import Builder

Builder.load_file("Inicio.kv")

class Iniciop(Screen):
    def on_enter(self):
        Clock.schedule_once(self.cargar_datos, 0)

    def cargar_datos(self, *args):
        app = App.get_running_app()
        self.usuario_id = getattr(app, 'usuario_id', None)

        if not self.usuario_id:
            self.ids.info_ultimo_entrenamiento.text = "Error: Usuario no encontrado."
            return

        self.mostrar_ultimo_rm(self.usuario_id)
        self.mostrar_grafica_rm()

    def mostrar_ultimo_rm(self, usuario_id):
        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT TOP 1 RM_Calculado, Ejercicio, Numero_Entrenamiento
            FROM Usuarios_RM
            WHERE Usuario = ?
            ORDER BY Numero_Entrenamiento DESC
        """, (usuario_id,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            rm_calculado, ejercicio_id, num_entrenamiento = resultado
            ejercicio_nombre = self.obtener_nombre_ejercicio(ejercicio_id)
            self.ids.info_ultimo_entrenamiento.text = (
                f"Último RM: {rm_calculado} en ejercicio '{ejercicio_nombre}'\n"
                f"Entrenamiento N°: {num_entrenamiento}"
            )
            self.ejercicio_seleccionado = ejercicio_id
        else:
            self.ids.info_ultimo_entrenamiento.text = "No hay registros disponibles."
            self.ids.grafica_rm.source = ""

    def obtener_nombre_ejercicio(self, ejercicio_id):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre FROM Ejercicios WHERE Id = ?", (ejercicio_id,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else "Desconocido"

    def mostrar_grafica_rm(self):
        if not hasattr(self, 'ejercicio_seleccionado') or not self.usuario_id:
            self.ids.info_ultimo_entrenamiento.text = "Seleccione ejercicio y usuario válido"
            self.ids.grafica_rm.source = ""
            return

        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Numero_Entrenamiento, RM_Calculado
            FROM Usuarios_RM
            WHERE Usuario = ? AND Ejercicio = ?
            ORDER BY Numero_Entrenamiento ASC
        """, (self.usuario_id, self.ejercicio_seleccionado))
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            self.ids.info_ultimo_entrenamiento.text = "No hay registros disponibles."
            self.ids.grafica_rm.source = ""
            return

        entrenamientos, rm_values = zip(*resultados)
        self.graficar_rm(list(entrenamientos), list(rm_values))

    def graficar_rm(self, entrenamientos, rm_values):
        plt.figure(figsize=(10, 4), dpi=100)
        ax = plt.gca()
        ax.set_facecolor((0.1, 0.1, 0.1))
        ax.grid(True, linestyle="--", color="gray", alpha=0.6)
        ax.plot(entrenamientos, rm_values, marker="o", color="cyan", linewidth=3)
        ax.scatter(entrenamientos[-1], rm_values[-1], color="red", s=100)

        ax.set_title("Progreso de RM", color="white")
        ax.set_xlabel("Número de Entrenamiento", color="white")
        ax.set_ylabel("RM Calculado", color="white")
        ax.tick_params(colors="white")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()
        ruta_imagen = os.path.join(os.getcwd(), "grafica_rm.png")
        plt.savefig(ruta_imagen, transparent=True)
        plt.close()

        if os.path.exists(ruta_imagen):
            self.ids.grafica_rm.source = ruta_imagen
            self.ids.grafica_rm.reload()
        else:
            self.ids.grafica_rm.source = ""
