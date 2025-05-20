from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivymd.uix.screen import MDScreen

from ConBD import crear_conexion


def obtener_grupos_musculares():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT DISTINCT Nombre FROM Musculos")
    resultados = cursor.fetchall()
    conexion.close()
    return [row[0] for row in resultados]


def obtener_ejercicios_por_grupo(nombre_grupo_muscular):
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT ID FROM Musculos WHERE Nombre = ?", (nombre_grupo_muscular,))
    id_musculo = cursor.fetchone()
    if not id_musculo:
        conexion.close()
        return []

    id_musculo = id_musculo[0]

    consulta = """
        SELECT DISTINCT E.Nombre
        FROM Ejercicios E
        JOIN Ejercicios_Musculos EM ON E.ID = EM.Ejercicio
        WHERE EM.Musculo = ?
    """
    cursor.execute(consulta, (id_musculo,))
    resultados = cursor.fetchall()
    conexion.close()
    return [row[0] for row in resultados]


class MenuScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        app.desde_login = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        self.add_widget(self.layout)

        self.layout.add_widget(MDLabel(
            text='Selecciona un grupo muscular',
            halign='center',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            font_style='H5'
        ))

        grupos = obtener_grupos_musculares()

        for grupo in grupos:
            btn = MDRaisedButton(
                text=grupo,
                size_hint=(1, None),
                height=50,
                md_bg_color=(1, 0.5, 0, 1),
                pos_hint={"center_x": 0.5}
            )
            btn.bind(on_release=self.select_group)
            self.layout.add_widget(btn)

        back_btn = MDRaisedButton(
            text='Volver a Inicio',
            md_bg_color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5}
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'pantalla11'))
        self.layout.add_widget(back_btn)

    def select_group(self, instance):
        selected_group = instance.text
        self.manager.get_screen('exercises').load_exercises_from_db(selected_group)
        self.manager.current = 'exercises'


class ExerciseScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

    def load_exercises_from_db(self, grupo_muscular):
        self.layout.clear_widgets()
        self.layout.add_widget(MDLabel(
            text=f"Ejercicios para {grupo_muscular}",
            halign='center',
            font_style='H5'
        ))

        ejercicios = obtener_ejercicios_por_grupo(grupo_muscular)
        for ex in ejercicios:
            btn = MDRaisedButton(text=ex, size_hint=(1, None), height=50)
            btn.bind(on_release=lambda inst, e=ex: self.goto_workout(e))
            self.layout.add_widget(btn)

        back_btn = MDRaisedButton(
            text='Volver',
            md_bg_color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=50
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(back_btn)

    def goto_workout(self, exercise_name):
        self.manager.get_screen('workout').set_exercise(exercise_name)
        self.manager.current = 'workout'


class WorkoutScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        app.desde_login = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        self.image1 = Image(source='', size_hint=(1, 0.4))
        self.image2 = Image(source='', size_hint=(1, 0.4))

        self.recommend_label = MDLabel(text='Series recomendadas:', halign='center')
        self.series_input = MDTextField(hint_text='¿Cuántas series harás?', mode='rectangle')
        self.series_input.bind(on_text_validate=self.update_series_inputs)
        self.series_container = MDBoxLayout(orientation='vertical', spacing=5)

        self.save_btn = MDRaisedButton(text='Guardar en BD', md_bg_color=(0, 1, 0, 1))
        self.save_btn.bind(on_release=self.guardar_series_en_bd)

        self.layout.add_widget(self.image1)
        self.layout.add_widget(self.image2)
        self.layout.add_widget(self.recommend_label)
        self.layout.add_widget(self.series_input)
        self.layout.add_widget(self.series_container)
        self.layout.add_widget(self.save_btn)

        back_btn = MDRaisedButton(text='Volver', md_bg_color=(1, 0, 0, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'exercises'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def set_exercise(self, exercise_name):
        self.exercise_name = exercise_name
        self.series_input.text = ''
        self.series_container.clear_widgets()
        self.recommend_label.text = f"Series recomendadas para {exercise_name}:"
        self.image1.source = 'RutinaMusculos/Pecho/Pectoral Mayor/Pectoral-mayor.gif'
        self.image2.source = 'assets/press_banca.gif'
        self.image1.reload()
        self.image2.reload()

    def update_series_inputs(self, instance):
        self.series_container.clear_widgets()
        try:
            self.num_series = int(self.series_input.text)
        except ValueError:
            return

        self.series_inputs = []
        for i in range(self.num_series):
            row = MDBoxLayout(orientation='horizontal', spacing=10)
            peso_input = MDTextField(hint_text=f'Serie {i+1} - Peso (kg)', mode='rectangle', size_hint_x=0.5)
            reps_input = MDTextField(hint_text=f'Serie {i+1} - Reps', mode='rectangle', size_hint_x=0.5)
            row.add_widget(peso_input)
            row.add_widget(reps_input)
            self.series_inputs.append((peso_input, reps_input))
            self.series_container.add_widget(row)

    def guardar_series_en_bd(self, instance):
        try:
            # Validar que todos los campos estén llenos
            for peso_input, reps_input in self.series_inputs:
                if not peso_input.text.strip() or not reps_input.text.strip():
                    from kivymd.uix.dialog import MDDialog
                    from kivymd.uix.button import MDFlatButton

                    def cerrar_dialogo(obj):
                        dialog.dismiss()

                    dialog = MDDialog(
                        text="Por favor, completa todos los campos de peso y repeticiones.",
                        buttons=[MDFlatButton(text="OK", on_release=cerrar_dialogo)]
                    )
                    dialog.open()
                    return

            conexion = crear_conexion()
            cursor = conexion.cursor()

            # Obtener el ID del ejercicio
            cursor.execute("SELECT ID FROM Ejercicios WHERE Nombre = ?", (self.exercise_name,))
            ejercicio_id = cursor.fetchone()[0]

            # Obtener el ID del usuario
            usuario_id = MDApp.get_running_app().usuario_id

            # Obtener el ID de la sesión más reciente (la que se acaba de crear)
            cursor.execute("""
                SELECT TOP 1 Id, Numero_de_Sesion 
                FROM Sesiones 
                WHERE Usuario = ? 
                ORDER BY Fecha DESC, Id DESC
            """, (usuario_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise Exception("No se encontró una sesión válida para el usuario.")

            sesion_id, numero_sesion = resultado

            rm_max = 0
            serie_rm_max = 0

            # Insertar las series en la base de datos
            for i, (peso_input, reps_input) in enumerate(self.series_inputs):
                peso = float(peso_input.text.strip())
                repeticiones = int(reps_input.text.strip())
                rm = round(peso * (1 + repeticiones / 30), 2)

                if rm > rm_max:
                    rm_max = rm
                    serie_rm_max = i + 1
                print(numero_sesion)
                cursor.execute("""
                    INSERT INTO Series (Ejercicio, Numero, Peso, Repeticiones, Numero_Entrenamiento, Sesion, Usuario)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (ejercicio_id, i + 1, peso, repeticiones, numero_sesion, numero_sesion, usuario_id))

            # Obtener el RM anterior
            cursor.execute("""
                SELECT TOP 1 RM_Calculado FROM Usuarios_RM 
                WHERE Usuario = ? AND Ejercicio = ?
                ORDER BY Numero_de_Sesion DESC
            """, (usuario_id, ejercicio_id))
            resultado = cursor.fetchone()
            rm_anterior = resultado[0] if resultado else None

            # Determinar el estado del nuevo RM
            if rm_anterior is None or rm_max > rm_anterior:
                estado_rm = "Sobresaliente"
            elif rm_max < rm_anterior:
                estado_rm = "Menos"
            else:
                estado_rm = "Constante"

            # Insertar el nuevo RM
            cursor.execute("""
                INSERT INTO Usuarios_RM (Usuario, Ejercicio, Numero_Entrenamiento, Numero_de_Serie, Numero_de_Sesion, RM_Calculado, Estado_RM)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (usuario_id, ejercicio_id, numero_sesion, serie_rm_max, sesion_id, rm_max, estado_rm))

            conexion.commit()
            conexion.close()

            self.manager.current = 'pantalla11'

        except Exception as e:
            print("Error guardando series:", e)
