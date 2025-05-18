from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import NumericProperty, StringProperty, ListProperty
from ConBD import crear_conexion
from matplotlib.ticker import MaxNLocator
from kivy.metrics import dp
import matplotlib.pyplot as plt
from kivy.lang import Builder
Builder.load_file("Stats.kv")

class Statsp(Screen):
    def limpiar_campos(self):
        self.ids.campo_ejercicio.text = ""
        self.ids.info_ultimo_entrenamiento.text = ""
        self.ids.grafica_rm.source = ""
        self.ejercicio_seleccionado = ""
    def on_enter(self):
        # Si usuario_id no está definido, usa usuario autenticado
        app = App.get_running_app()
        if not self.usuario_id:
            # Intentamos obtener ID desde usuario_actual (nombre de usuario)
            self.usuario_id = self.get_usuario_id_por_nombre(app.usuario_actual)
        print(f"ROL ACTUAL: {self.rol}")  # DEBUG
        self.cargar_ejercicios()
        btn = self.ids.btn_imprimir
        if self.rol == 1:
            btn.opacity = 1
            btn.disabled = False
            btn.md_bg_color = (0, 1, 0, 1)  # verde
            btn.text_color = (1, 1, 1, 1) 
        else:
            btn.opacity = 0
            btn.disabled = True
    rol = NumericProperty(2)
    ejercicio_seleccionado = StringProperty("")
    menu_items = ListProperty([])
    menu = None

    usuario_id = None  # Aquí guardamos el usuario para el que mostramos estadísticas

    def get_usuario_id_por_nombre(self, nombre_usuario):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT Id FROM Usuarios WHERE Nombre_Usuario = ?", (nombre_usuario,))
        res = cursor.fetchone()
        conn.close()
        if res:
            return res[0]
        return None

    def cargar_ejercicios(self):
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre FROM Ejercicios ORDER BY Nombre")
        ejercicios = [r[0] for r in cursor.fetchall() if r[0]]
        conn.close()

        self.menu_items = [
            {
                "text": e,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=e: self.seleccionar_ejercicio(x),
            }
            for e in ejercicios
        ]

        if not self.menu:
            from kivymd.uix.menu import MDDropdownMenu

            self.menu = MDDropdownMenu(
                caller=self.ids.campo_ejercicio, items=self.menu_items, width_mult=4
            )
        else:
            self.menu.items = self.menu_items

        # Seleccionar el primero si no hay seleccionado
        if ejercicios and not self.ejercicio_seleccionado:
            self.seleccionar_ejercicio(ejercicios[0])

    def seleccionar_ejercicio(self, ejercicio):
        self.ejercicio_seleccionado = ejercicio
        self.ids.campo_ejercicio.text = ejercicio
        self.mostrar_grafica_rm()

    def mostrar_grafica_rm(self):
        if not self.ejercicio_seleccionado or not self.usuario_id:
            self.ids.info_ultimo_entrenamiento.text = "Seleccione ejercicio y usuario válido"
            self.ids.grafica_rm.source = ""
            return

        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT ur.Numero_Entrenamiento, ur.RM_Calculado
            FROM Usuarios_RM ur
            JOIN Ejercicios e ON ur.Ejercicio = e.Id
            WHERE ur.Usuario = ? AND e.Nombre = ?
            ORDER BY ur.Numero_Entrenamiento ASC
            """,
            (self.usuario_id, self.ejercicio_seleccionado),
        )
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            self.ids.info_ultimo_entrenamiento.text = "No hay registros disponibles."
            self.ids.grafica_rm.source = ""
            return

        entrenamientos, rm_values = zip(*resultados)
        self.graficar_rm(list(entrenamientos), list(rm_values))

        # Mostrar la última vez que se hizo el ejercicio y con qué peso
        ultimo_entrenamiento = entrenamientos[-1]
        ultimo_rm = rm_values[-1]
        self.ids.info_ultimo_entrenamiento.text = (
            f"Último entrenamiento: {ultimo_entrenamiento} con RM: {ultimo_rm}"
        )

    def graficar_rm(self, entrenamientos, rm_values):
        plt.figure(figsize=(10, 4), dpi=100)
        ax = plt.gca()
        ax.plot(entrenamientos, rm_values, marker="o", color="white", linewidth=3)
        ax.scatter(entrenamientos[-1], rm_values[-1], color="red", s=100)
        ax.set_title("Progreso de RM", color="white")
        ax.set_xlabel("Número de Entrenamiento", color="white")
        ax.set_ylabel("RM Calculado", color="white")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.set_facecolor((0.15, 0.15, 0.15))
        ax.tick_params(colors="white")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.tight_layout()
        plt.savefig("grafica_rm.png", transparent=True)
        plt.close()

        self.ids.grafica_rm.source = "grafica_rm.png"
        self.ids.grafica_rm.reload()

    def reset_usuario(self):
        # Usar para limpiar la selección si quieres
        self.usuario_id = None
        self.ejercicio_seleccionado = ""
        self.ids.campo_ejercicio.text = ""
        self.ids.info_ultimo_entrenamiento.text = ""
        self.ids.grafica_rm.source = ""

    def cambiar_vista(self):
        if self.ids.imagen_musculos.opacity == 0:
            # Mostrar imagen de músculos
            self.ids.imagen_musculos.opacity = 1
            self.ids.contenedor_scroll.opacity = 0
            self.ids.campo_ejercicio.opacity = 0
            self.ids.info_ultimo_entrenamiento.opacity = 0
        else:
            # Mostrar gráfica y controles
            self.ids.imagen_musculos.opacity = 0
            self.ids.contenedor_scroll.opacity = 1
            self.ids.campo_ejercicio.opacity = 1
            self.ids.info_ultimo_entrenamiento.opacity = 1



