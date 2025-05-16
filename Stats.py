import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from PIL import Image, ImageDraw
from kivy.properties import NumericProperty
import numpy as np
from ConBD import crear_conexion

# Crear imágenes iniciales si no existen
Image.new('RGB', (800, 400), color='white').save("grafica_rm.png")
Image.new('RGB', (800, 800), color='white').save("musculos_base.png")

# Cargar archivo KV
Builder.load_file("Stats.kv")

class Statsp(Screen):
    rol = NumericProperty(2)
    def on_enter(self):
        self.mostrar_grafica_rm()
        self.mostrar_imagen_musculos()

    def mostrar_grafica_rm(self):
        conn = crear_conexion()
        cursor = conn.cursor()

        # Obtener ID del usuario
        cursor.execute("SELECT Id FROM Usuarios WHERE Nombre_Usuario = ?", (App.get_running_app().usuario_actual,))
        usuario_id = cursor.fetchone()

        if not usuario_id:
            print("❌ Usuario no encontrado.")
            conn.close()
            return

        usuario_id = usuario_id[0]

        # Obtener datos del RM
        cursor.execute("SELECT Numero_Entrenamiento, RM_Calculado FROM Usuarios_RM WHERE Usuario = ? ORDER BY Numero_Entrenamiento ASC", (usuario_id,))
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            return

        entrenamientos = [r[0] for r in resultados]
        rm_values = [r[1] for r in resultados]

        plt.figure(figsize=(8, 4))
        plt.plot(entrenamientos, rm_values, marker='o', color='green')
        plt.title("Progreso de RM")
        plt.xlabel("Número de Entrenamiento")
        plt.ylabel("RM Calculado")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig("grafica_rm.png")
        plt.close()

        self.ids.grafica_rm.source = "grafica_rm.png"
        self.ids.grafica_rm.reload()

    def mostrar_imagen_musculos(self):
        imagen_base = Image.open("musculos_base.png").convert("RGBA")
        dibujar = ImageDraw.Draw(imagen_base, "RGBA")

        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute("SELECT Id FROM Usuarios WHERE Nombre_Usuario = ?", (App.get_running_app().usuario_actual,))
        usuario_id = cursor.fetchone()

        if not usuario_id:
            conn.close()
            return

        usuario_id = usuario_id[0]

        cursor.execute("SELECT E.Nombre, RM_Calculado FROM Usuarios_RM URM JOIN Ejercicios E ON URM.Ejercicio = E.Id WHERE Usuario = ?", (usuario_id,))
        resultados = cursor.fetchall()
        conn.close()

        colores = {"alto": (0, 255, 0, 150), "medio": (255, 255, 0, 150), "bajo": (255, 0, 0, 150)}

        areas_musculares = {"Pecho": [(200, 150), (300, 200)], "Espalda": [(200, 50), (300, 100)], "Piernas": [(200, 400), (300, 500)]}

        for ejercicio, rm in resultados:
            if rm >= 100:
                color = colores["alto"]
            elif rm >= 70:
                color = colores["medio"]
            else:
                color = colores["bajo"]

            area = areas_musculares.get(ejercicio, None)
            if area:
                dibujar.rectangle(area, fill=color)

        imagen_base.save("musculos_dinamicos.png")
        self.ids.imagen_musculos.source = "musculos_dinamicos.png"
        self.ids.imagen_musculos.reload()
