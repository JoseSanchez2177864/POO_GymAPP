from kivymd.app import MDApp
from datetime import datetime
from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
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
        self.ids.ejercicios_container.clear_widgets()

        usuario_id = App.get_running_app().usuario_id 
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            consulta = """
            SELECT e.Nombre, s.Numero, s.Peso, s.Repeticiones, s.Id
            FROM Series s
            JOIN Ejercicios e ON s.Ejercicio = e.Id
            WHERE s.Usuario = ? AND s.Sesion = ?
            ORDER BY e.Nombre, s.Numero
            """
            cursor.execute(consulta, (usuario_id, self.nueva_sesion))
            resultados = cursor.fetchall()

            from collections import OrderedDict
            agrupado = OrderedDict()
            for nombre_ej, num_serie, peso, reps, serie_id in resultados:
                if nombre_ej not in agrupado:
                    agrupado[nombre_ej] = []
                agrupado[nombre_ej].append((num_serie, peso, reps, serie_id))

            for nombre_ej, series in agrupado.items():
                label_ej = MDLabel(
                    text=f"[b]{nombre_ej}[/b]",
                    markup=True,
                    size_hint_y=None,
                    height=dp(30),
                    theme_text_color="Primary"
                )
                self.ids.ejercicios_container.add_widget(label_ej)

                for num_serie, peso, reps, serie_id in series:
                    box = MDBoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=dp(25),
                        spacing=dp(10)
                    )
                    label_serie = MDLabel(text=f"Serie {num_serie}", size_hint_x=0.2)
                    label_peso = MDLabel(text=f"Peso: {peso} kg", size_hint_x=0.3)
                    label_reps = MDLabel(text=f"Reps: {reps}", size_hint_x=0.3)
                    box.add_widget(label_serie)
                    box.add_widget(label_peso)
                    box.add_widget(label_reps)

                    # Botón modificar
                    btn_modificar = MDIconButton(
                        icon="pencil",
                        user_font_size="20sp",
                        size_hint=(None, None),
                        size=(dp(30), dp(30)),
                        pos_hint={'center_y': 0.5},
                    )
                    btn_modificar.bind(
                        on_release=lambda inst, sid=serie_id, p=peso, r=reps: self.abrir_popup_modificar(sid, p, r)
                    )
                    box.add_widget(btn_modificar)

                    self.ids.ejercicios_container.add_widget(box)

            if not resultados:
                container = MDBoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(200),
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


    def abrir_popup_modificar(self, serie_id, peso_actual, reps_actual):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.core.window import Window

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        titulo = MDLabel(
            text="Modificar Serie",
            size_hint_y=None,
            height=30,
            font_style="H6",
            halign='center'
        )
        layout.add_widget(titulo)

        self.peso_input = MDTextField(
            hint_text="Peso (kg)",
            text=str(peso_actual),
            mode="rectangle",
            input_filter='float',
            size_hint_y=None,
            height=40
        )
        self.reps_input = MDTextField(
            hint_text="Repeticiones",
            text=str(reps_actual),
            mode="rectangle",
            input_filter='int',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.peso_input)
        layout.add_widget(self.reps_input)

        btn_guardar = MDRaisedButton(
            text="Guardar",
            size_hint=(1, None),
            height=40,
            md_bg_color=(0, 0.5, 1, 1)
        )
        btn_guardar.bind(on_release=lambda x: self.guardar_modificacion(serie_id))

        btn_cancelar = MDFlatButton(
            text="Cancelar",
            size_hint=(1, None),
            height=40,
            text_color=(1, 0, 0, 1)
        )
        btn_cancelar.bind(on_release=lambda x: self.popup.dismiss())

        layout.add_widget(btn_guardar)
        layout.add_widget(btn_cancelar)

        self.popup = ModalView(
            size_hint=(0.85, None),
            height=280,
            auto_dismiss=False,
            background_color=(0, 0, 0, 0.6)  # Fondo negro semitransparente
        )
        self.popup.add_widget(layout)
        self.popup.open()

    def guardar_modificacion(self, serie_id):
        try:
            nuevo_peso = float(self.peso_input.text)
            nuevas_reps = int(self.reps_input.text)
        except ValueError:
            print("Peso o repeticiones no válidos")
            return

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE Series SET Peso = ?, Repeticiones = ? WHERE Id = ?",
                (nuevo_peso, nuevas_reps, serie_id)
            )
            conexion.commit()
            print(f"Serie {serie_id} actualizada con peso {nuevo_peso} y reps {nuevas_reps}")
        except Exception as e:
            print(f"Error al actualizar serie: {e}")
        finally:
            cursor.close()
            conexion.close()

        self.popup.dismiss()
        self.cargar_series_sesion()
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
