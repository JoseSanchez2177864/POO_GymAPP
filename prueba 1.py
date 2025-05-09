from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# --- Datos del músculo, submúsculo y ejercicios ---
muscle_structure = {
    'Pecho': {
        'Pectoral mayor': ['Press banca', 'Press inclinado', 'Lagartijas'],
        'Pectoral menor': ['Press declinado', 'Fondos inclinados', 'Flyes hacia abajo']
    },
    'Espalda': {
        'Dorsal ancho': ['Remo unilateral o agarre V', 'Jalón al pecho', 'Dominadas'],
        'Trapecio': ['Encogimiento de hombro'],
        'Romboides': ['Remo con barra', 'Facepulls'],
        'Infraespinoso': ['Facepulls']
    },
    'Piernas': {
        'Cuádriceps': ['Sentadilla libre', 'Sentadilla Hack', 'Pendulum squat', 'Prensa', 'Extensiones de quadriceps'],
        'Femoral': ['Curl femoral acostado', 'Peso muerto rumano', 'Glute ham raise'],
        'Glúteos': ['Hip thrust', 'Sentadilla bulgara', 'Peso muerto convencional', 'Patada de glúteo'],
        'Gemelos': ['Elevación de talones de pie', 'Elevación de talones sentado'],
    },
    'Hombros': {
        'Deltoides posterior': ['Press militar', 'Elevaciones frontales'],
        'Deltoides lateral': ['Elevaciones laterales'],
        'Deltoides anterior': ['Pájaros', 'Facepulls', 'Cruce de poleas inverso'],
    },
    'Bíceps': {
        'Bíceps corto': ['Curl concentrado', 'Curl de bicep con barra', 'Curl de bicep con mancuernas'],
        'Braquial': ['Curl martillo'],
        'Bíceps largo': ['Curl araña', 'Curl inclinado'],
    },
    'Tríceps': {
        'Tríceps lateral': ['Extensiones de triceps con cuerda', 'Extensiones de triceps con barra'],
        'Tríceps largo': ['Press francés', 'Fondos'],
        'Tríceps medial': ['Extension Katana con polea'],
    }
}

# --- Pantallas ---
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='Selecciona un grupo muscular', font_size=24))

        for muscle in muscle_structure.keys():
            btn = Button(text=muscle)
            btn.bind(on_press=self.select_muscle)
            layout.add_widget(btn)

        self.add_widget(layout)

    def select_muscle(self, instance):
        selected = instance.text
        self.manager.get_screen('details').set_submuscles(selected)
        self.manager.current = 'details'

class MuscleDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

    def set_submuscles(self, muscle):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text=f"Submúsculos de {muscle}", font_size=22))
        for submuscle in muscle_structure[muscle].keys():
            btn = Button(text=submuscle)
            btn.bind(on_press=lambda instance, m=muscle, s=submuscle: self.show_exercises(m, s))
            self.layout.add_widget(btn)

        back_btn = Button(text='Volver')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(back_btn)

    def show_exercises(self, muscle, submuscle):
        self.manager.get_screen('exercises').set_exercises(muscle, submuscle)
        self.manager.current = 'exercises'

class ExerciseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

    def set_exercises(self, muscle, submuscle):
        self.layout.clear_widgets()
        title = f"Ejercicios para {submuscle}"
        self.layout.add_widget(Label(text=title, font_size=22))

        exercises = muscle_structure[muscle][submuscle]
        for ex in exercises:
            btn = Button(text=ex)
            btn.bind(on_press=lambda instance, e=ex: self.open_log_screen(e))
            self.layout.add_widget(btn)

        back_btn = Button(text='Volver')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'details'))
        self.layout.add_widget(back_btn)

    def open_log_screen(self, exercise_name):
        log_screen = self.manager.get_screen('log')
        log_screen.set_exercise(exercise_name)
        self.manager.current = 'log'

class LogExerciseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

    def set_exercise(self, exercise_name):
        self.layout.clear_widgets()
        self.exercise_name = exercise_name

        self.layout.add_widget(Label(text=f"Registro: {exercise_name}", font_size=20))

        # --- Imagenes ---
        img_layout = BoxLayout(size_hint_y=None, height=200, spacing=10)
        self.img1 = AsyncImage(source='', allow_stretch=True)
        self.img2 = AsyncImage(source='', allow_stretch=True)
        img_layout.add_widget(self.img1)
        img_layout.add_widget(self.img2)
        self.layout.add_widget(img_layout)

        # Puedes poner aquí tus URLs personalizadas más adelante:
        # self.img1.source = 'URL_IMAGEN_MUSCULO'
        # self.img2.source = 'URL_IMAGEN_EJERCICIO'

        # Series recomendadas (puedes editar esta parte tú)
        self.layout.add_widget(Label(text="Series recomendadas: ", font_size=16))

        # Ingreso de series
        series_input_layout = BoxLayout(size_hint_y=None, height=40)
        self.series_input = TextInput(hint_text="¿Cuántas series harás?", multiline=False, input_filter='int')
        self.series_input.bind(text=self.update_reps_fields)
        series_input_layout.add_widget(self.series_input)
        self.layout.add_widget(series_input_layout)

        # Aquí irán los campos de repeticiones
        self.reps_container = BoxLayout(orientation='vertical', spacing=5)
        self.layout.add_widget(self.reps_container)

        # Botón de volver
        back_btn = Button(text='Volver')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'exercises'))
        self.layout.add_widget(back_btn)

    def update_reps_fields(self, instance, value):
        self.reps_container.clear_widgets()
        try:
            num_series = int(value)
            for i in range(num_series):
                row = BoxLayout(size_hint_y=None, height=40)
                row.add_widget(Label(text=f"Reps serie {i+1}:"))
                row.add_widget(TextInput(hint_text="Reps", multiline=False, input_filter='int'))
                self.reps_container.add_widget(row)
        except ValueError:
            pass

# --- App Principal ---
class GymApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MuscleDetailScreen(name='details'))
        sm.add_widget(ExerciseScreen(name='exercises'))
        sm.add_widget(LogExerciseScreen(name='log'))
        return sm

if __name__ == '__main__':
    GymApp().run()
