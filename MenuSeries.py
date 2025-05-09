from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

# Pantalla de registro de ejercicio
class RegistroEjercicio(Screen):
    def __init__(self, nombre_ejercicio, link_musculo, link_ejercicio, series_recomendadas, **kwargs):
        super().__init__(name=nombre_ejercicio, **kwargs)
        self.series_inputs = []

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        imagenes = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=10)
        self.imagen_musculo = AsyncImage(source=link_musculo)
        self.imagen_ejercicio = AsyncImage(source=link_ejercicio)
        imagenes.add_widget(self.imagen_musculo)
        imagenes.add_widget(self.imagen_ejercicio)
        self.layout.add_widget(imagenes)

        self.series_label = Label(text=f"Series recomendadas: {series_recomendadas}", size_hint=(1, 0.1), font_size=18)
        self.layout.add_widget(self.series_label)

        self.series_input_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        self.series_input_row.add_widget(Label(text="¿Cuántas series harás?", size_hint=(0.6, 1)))
        self.num_series_input = TextInput(hint_text="Ej: 3", multiline=False, size_hint=(0.2, 1), input_filter='int')
        self.confirmar_btn = Button(text="Confirmar", size_hint=(0.2, 1))
        self.confirmar_btn.bind(on_press=self.crear_campos_series)
        self.series_input_row.add_widget(self.num_series_input)
        self.series_input_row.add_widget(self.confirmar_btn)
        self.layout.add_widget(self.series_input_row)

        self.series_container = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.4))
        self.layout.add_widget(self.series_container)

        self.guardar_btn = Button(text="Guardar", size_hint=(1, 0.1))
        self.guardar_btn.bind(on_press=self.guardar_registro)
        self.layout.add_widget(self.guardar_btn)

        self.add_widget(self.layout)

    def crear_campos_series(self, instance):
        self.series_container.clear_widgets()
        self.series_inputs.clear()

        try:
            num = int(self.num_series_input.text)
        except ValueError:
            return

        for i in range(num):
            fila = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, spacing=10)
            label = Label(text=f"Repeticiones S{i+1}:", size_hint=(0.4, 1))
            rep_input = TextInput(hint_text="Reps", multiline=False, size_hint=(0.3, 1), input_filter='int')
            peso_input = TextInput(hint_text="Peso (kg)", multiline=False, size_hint=(0.3, 1), input_filter='float')
            fila.add_widget(label)
            fila.add_widget(rep_input)
            fila.add_widget(peso_input)
            self.series_inputs.append((rep_input, peso_input))
            self.series_container.add_widget(fila)

    def guardar_registro(self, instance):
        datos = []
        for i, (rep_input, peso_input) in enumerate(self.series_inputs):
            rep = rep_input.text
            peso = peso_input.text
            datos.append((rep, peso))
            print(f"Serie {i+1}: {rep} reps, {peso} kg")

# Pantalla principal para simular navegación desde botón de ejercicio
class MenuPrincipal(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(name="menu", **kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(text='Selecciona un ejercicio de ejemplo')
        layout.add_widget(label)

        btn = Button(text="Press Banca")
        btn.bind(on_press=lambda x: self.ir_a_registro(screen_manager))
        layout.add_widget(btn)

        self.add_widget(layout)

    def ir_a_registro(self, sm):
        nombre = "Press Banca"
        link_musculo = "https://outlift.com/wp-content/uploads/2021/02/musculos-trabajados-press-de-banca.jpg"  # <-- reemplaza
        link_ejercicio = "https://www.masmusculo.com/blog/wp-content/uploads/2016/03/pressbanca.png"  # <-- reemplaza
        series = 4
        if not sm.has_screen(nombre):
            pantalla = RegistroEjercicio(nombre, link_musculo, link_ejercicio, series)
            sm.add_widget(pantalla)
        sm.current = nombre

class RegistroEjercicioApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuPrincipal(screen_manager=sm))
        return sm

if __name__ == '__main__':
    RegistroEjercicioApp().run()
