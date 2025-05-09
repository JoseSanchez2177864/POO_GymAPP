from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# Datos del músculo, submúsculo y ejercicios
muscle_structure = {
    'Pecho': {
        'Pectoral mayor': ['Press banca', 'Press inclinado', 'Lagartijas', ],
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
            btn.bind(on_press=self.select_exercise)
            self.layout.add_widget(btn)

        back_btn = Button(text='Volver')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'details'))
        self.layout.add_widget(back_btn)

    def select_exercise(self, instance):
        print(f"Ejercicio seleccionado: {instance.text}")
        # Aquí luego se puede redirigir a una nueva pantalla para registrar reps y peso

class GymApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MuscleDetailScreen(name='details'))
        sm.add_widget(ExerciseScreen(name='exercises'))
        return sm

if __name__ == '__main__':
    GymApp().run()


py -3.11 --version
