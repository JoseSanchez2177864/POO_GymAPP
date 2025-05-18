from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.modalview import ModalView  # Esta es de Kivy, no de KivyMD
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp

Builder.load_file("InEntra.kv")

class InEntrap(MDScreen):
    def on_enter(self):
        self.tiempo = 0
        self.evento_cronometro = Clock.schedule_interval(self.actualizar_cronometro, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tiempo = 0
        Clock.schedule_interval(self.actualizar_cronometro, 1)

    def actualizar_cronometro(self, dt):
        self.tiempo += 1
        minutos = self.tiempo // 60
        segundos = self.tiempo % 60
        self.ids.cronometro_label.text = f"{minutos:02}:{segundos:02}"


    def finalizar_entrenamiento(self):
        # Detener el cronómetro si está corriendo
        if hasattr(self, 'evento_cronometro'):
            self.evento_cronometro.cancel()

        # Crear el popup estilizado
        popup = ModalView(size_hint=(0.85, 0.45), auto_dismiss=False, background_color=(0, 0, 0, 0))

        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20),
            size_hint=(None, None),
            size=(dp(300), dp(200)),
            md_bg_color=(0.12, 0.12, 0.12, 1),
            radius=[20, 20, 20, 20],
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        label = MDLabel(
            text="🎉 ¡Entrenamiento finalizado!\n¡Buen trabajo!",
            halign="center",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
        )

        boton = MDRaisedButton(
            text="Aceptar",
            md_bg_color=(0.8, 0.1, 0.1, 1),
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
            on_release=lambda *args: self.salir_al_inicio(popup)
        )

        card.add_widget(label)
        card.add_widget(boton)
        popup.add_widget(card)
        popup.open()

    def salir_al_inicio(self, popup):
        popup.dismiss()
        self.manager.current = 'pantalla3'
