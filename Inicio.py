import os
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from ConBD import crear_conexion
from kivy.lang import Builder

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_file("Inicio.kv")

class Iniciop(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        app.desde_login = False

        Clock.schedule_once(self.cargar_datos, 0)

        if app.rol_actual == 1:
            self.mostrar_boton_añadir()

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

    def mostrar_boton_añadir(self):
        # Verifica si ya se ha creado el botón previamente
        if hasattr(self, 'boton_añadir') and self.boton_añadir in self.ids.box_contenido.children:
            return

        self.boton_añadir = MDRaisedButton(
            text="Añadir Ejercicio",
            size_hint=(1, None),
            height=50,
            md_bg_color=(0.2, 0.4, 0.7, 1),
            on_release=self.mostrar_popup_añadir_ejercicio
        )
        # Lo colocamos arriba (inicio del layout vertical)
        self.ids.box_contenido.add_widget(self.boton_añadir, index=len(self.ids.box_contenido.children))

    def mostrar_popup_añadir_ejercicio(self, *args):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.widget import Widget
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        from kivy.uix.modalview import ModalView

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        titulo = Label(
            text="Añadir Ejercicio",
            size_hint_y=None,
            height=30,
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True,
            halign='center'
        )
        titulo.bind(size=lambda s, w: setattr(s, 'text_size', w))
        layout.add_widget(titulo)

        self.input_nombre_ejercicio = MDTextField(
            hint_text='Nombre del ejercicio',
            mode='rectangle'
        )
        self.input_descripcion_ejercicio = MDTextField(
            hint_text='Descripción',
            mode='rectangle'
        )
        self.input_musculo_ejercicio = MDTextField(
            hint_text='Músculo trabajado',
            mode='rectangle'
        )

        layout.add_widget(self.input_nombre_ejercicio)
        layout.add_widget(self.input_descripcion_ejercicio)
        layout.add_widget(self.input_musculo_ejercicio)

        layout.add_widget(Widget(size_hint_y=None, height=40))

        guardar_btn = MDRaisedButton(
            text='Guardar',
            size_hint=(0.4, None),
            height=45,
            md_bg_color="green"
        )
        guardar_btn.bind(on_release=self.guardar_ejercicio)

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

        self.popup = ModalView(
            size_hint=(0.9, None),
            height=480,
            auto_dismiss=False,
            background_color=(0, 0, 0, 0.7)
        )
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nombre FROM Musculos")
        musculos = cursor.fetchall()
        conn.close()

        menu_items = [{
            "text": descripcion,
            "viewclass": "OneLineListItem",
            "on_release": lambda x=descripcion, y=id_: self.set_musculo(x, y)
        } for id_, descripcion in musculos]

        self.menu_musculos = MDDropdownMenu(
            caller=self.input_musculo_ejercicio,
            items=menu_items,
            width_mult=4
        )

        self.input_musculo_ejercicio.bind(
            focus=lambda instance, value: self.menu_musculos.open() if value else None
        )

        self.popup.add_widget(layout)
        self.popup.open()

    def set_musculo(self, nombre, musculo_id):
        self.input_musculo_ejercicio.text = nombre
        self.musculo_id_seleccionado = musculo_id
        self.menu_musculos.dismiss()

    def guardar_ejercicio(self, *args):
        nombre = self.input_nombre_ejercicio.text.strip()
        descripcion = self.input_descripcion_ejercicio.text.strip()
        musculo_id = getattr(self, 'musculo_id_seleccionado', None)

        if not nombre or not descripcion or musculo_id is None:
            print("Faltan campos obligatorios.")
            return

        try:
            conn = crear_conexion()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Ejercicios (Nombre, Descripcion)
                OUTPUT INSERTED.Id
                VALUES (?, ?)
            """, (nombre, descripcion))
            ejercicio_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO Ejercicios_Musculos (Ejercicio, Musculo)
                VALUES (?, ?)
            """, (ejercicio_id, musculo_id))

            conn.commit()
            conn.close()
            self.popup.dismiss()
            print("Ejercicio creado exitosamente.")
        except Exception as e:
            print(f"Error al guardar ejercicio: {e}")


