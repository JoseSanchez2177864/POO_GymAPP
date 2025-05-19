from kivymd.app import MDApp
from datetime import datetime
from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from ConBD import crear_conexion

Builder.load_file("InEntra.kv")

class InEntrap(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tiempo = 0
        Clock.schedule_interval(self.actualizar_cronometro, 1)
        self.nueva_sesion = None

    def on_pre_enter(self):
        app = MDApp.get_running_app()
        if app.desde_login == False:
            self.crear_nueva_sesion()
            app.desde_login = False 
        self.cargar_series_sesion()

    def on_enter(self):
        self.tiempo = 0
        self.cargar_series_sesion()
        self.evento_cronometro = Clock.schedule_interval(self.actualizar_cronometro, 1)
    
    def actualizar_cronometro(self, dt):
        self.tiempo += 1
        minutos = self.tiempo // 60
        segundos = self.tiempo % 60
        self.ids.cronometro_label.text = f"{minutos:02}:{segundos:02}"

    def crear_nueva_sesion(self):
        usuario_id = MDApp.get_running_app().usuario_id 
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            cursor.execute("SELECT ISNULL(MAX(Numero_de_Sesion), 0) + 1 FROM Sesiones WHERE Usuario = ?", (usuario_id,))
            nueva_sesion = cursor.fetchone()[0]  # guarda en variable temporal

            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                "INSERT INTO Sesiones (Usuario, Numero_de_Sesion, Fecha) VALUES (?, ?, ?)", 
                (usuario_id, nueva_sesion, fecha_actual)
            )
            conexion.commit()

            self.nueva_sesion = nueva_sesion  # solo aquí si todo va bien
            print(f"Nueva sesión creada: Usuario {usuario_id}, Sesión {self.nueva_sesion}, Fecha {fecha_actual}")

        except Exception as e:
            print(f"Error al crear la nueva sesión: {e}")
            self.nueva_sesion = None  # opcional: dejar explícito

        finally:
            cursor.close()
            conexion.close()


    def cargar_series_sesion(self):
        """
        Carga y muestra las series de la sesión actual, agrupadas por ejercicio.
        """
        self.ids.ejercicios_container.clear_widgets()

        usuario_id = App.get_running_app().usuario_id 
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            # Consultar series y ejercicios para la sesión actual
            # Ajusta la consulta según tu esquema y nombres de tablas/columnas
            consulta = """
            SELECT e.Nombre, s.Numero, s.Peso, s.Repeticiones
            FROM Series s
            JOIN Ejercicios e ON s.Ejercicio = e.Id
            JOIN Sesiones ses ON s.Sesion = ses.Numero_de_Sesion AND ses.Usuario = ?
            WHERE ses.Numero_de_Sesion = ?
            ORDER BY e.Nombre, s.Numero
            """
            cursor.execute(consulta, (usuario_id, self.nueva_sesion))
            resultados = cursor.fetchall()
            print(self.nueva_sesion)
            print(resultados)

            # Agrupar por ejercicio
            from collections import OrderedDict
            agrupado = OrderedDict()
            for nombre_ej, num_serie, peso, reps in resultados:
                if nombre_ej not in agrupado:
                    agrupado[nombre_ej] = []
                agrupado[nombre_ej].append((num_serie, peso, reps))

            # Crear widgets para mostrarlo
            for nombre_ej, series in agrupado.items():
                # Título ejercicio
                label_ej = MDLabel(
                    text=f"[b]{nombre_ej}[/b]",
                    markup=True,
                    size_hint_y=None,
                    height=dp(30),
                    theme_text_color="Primary"
                )
                self.ids.ejercicios_container.add_widget(label_ej)

                # Series
                for num_serie, peso, reps in series:
                    box = MDBoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=dp(25),
                        spacing=dp(10)
                    )
                    label_serie = MDLabel(text=f"Serie {num_serie}", size_hint_x=0.3)
                    label_peso = MDLabel(text=f"Peso: {peso} kg", size_hint_x=0.4)
                    label_reps = MDLabel(text=f"Reps: {reps}", size_hint_x=0.3)
                    box.add_widget(label_serie)
                    box.add_widget(label_peso)
                    box.add_widget(label_reps)

                    self.ids.ejercicios_container.add_widget(box)

            if not resultados:
                # Creamos un contenedor más grande para el mensaje
                container = MDBoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(200),  # Puedes ajustar esta altura según tus necesidades
                    padding=dp(20)
                )
                mensaje = MDLabel(
                    text="No hay series registradas para esta sesión.",
                    halign="center",
                    font_style="H6",
                    theme_text_color="Primary"
                )
                container.add_widget(mensaje)
                self.ids.ejercicios_container.add_widget(container)


        except Exception as e:
            print(f"Error al cargar series: {e}")
        finally:
            cursor.close()
            conexion.close()

    def finalizar_entrenamiento(self, instance=None):
        popup = ModalView(size_hint=(0.8, None), height=dp(200))

        box = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        mensaje = MDLabel(
            text="¡Felicidades, has finalizado tu entrenamiento!",
            halign='center',
            theme_text_color="Primary",
            font_style="H6"
        )
        box.add_widget(mensaje)

        btn_cerrar = MDRaisedButton(
            text="Cerrar",
            on_release=lambda x: popup.dismiss()
        )
        box.add_widget(btn_cerrar)

        popup.add_widget(box)

        def on_dismiss(*args):
            self.manager.current = 'pantalla3'

        popup.bind(on_dismiss=on_dismiss)
        popup.open()
