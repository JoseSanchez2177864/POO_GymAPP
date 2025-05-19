# app.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
Window.size = (360, 640)  # Tamaño típico de un móvil
from InS import InSp
from CrS import CrSp
from Inicio import Iniciop
from Entr import Entrp
from Config import Configp
from Stats import Statsp
from CRUDu import CRUDup
from CRUDp import CRUDpp
from Planes import Planesp
from StatsAdmin import StatsAdminp
from InEntra import InEntrap
from Ej1Entra import MenuScreen, ExerciseScreen, WorkoutScreen

import kivymd
print("Hola aquí esta la version:",kivymd.__version__)

class GymApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        self.desde_login = False
        self.pantalla_origen = ""
        # Cargar archivos .kv después de inicializar la app
        Builder.load_file("InS.kv")
        Builder.load_file("CrS.kv")
        sm = ScreenManager()
        sm.add_widget(InSp(name='pantalla1'))
        sm.add_widget(CrSp(name='pantalla2'))
        sm.add_widget(Iniciop(name='pantalla3'))
        sm.add_widget(Entrp(name='pantalla4'))
        sm.add_widget(Configp(name='pantalla5'))
        sm.add_widget(Statsp(name='pantalla6'))
        sm.add_widget(CRUDup(name='pantalla7'))
        sm.add_widget(CRUDpp(name='pantalla8'))
        sm.add_widget(Planesp(name='pantalla9'))
        sm.add_widget(StatsAdminp(name='pantalla10'))
        sm.add_widget(InEntrap(name='pantalla11'))
        sm.add_widget(MenuScreen(name='menu'))         # pantalla13
        sm.add_widget(ExerciseScreen(name='exercises'))     # pantalla15
        sm.add_widget(WorkoutScreen(name='workout')) 

        sm.current = 'pantalla1'
        return sm
    
    def redirigir_por_rol(self):
        if self.rol_actual == 1:
            self.root.current = 'pantalla8'  # Pantalla para administradores
        elif self.rol_actual == 2:
            self.root.current = 'pantalla9'
    def redirigir_por_rol2(self):
        if self.rol_actual == 1:
            self.root.current = 'pantalla10'  # Pantalla para administradores
        elif self.rol_actual == 2:
            self.root.current = 'pantalla6'
    def cambiar_pantalla(self, nombre_pantalla):
        self.root.current = nombre_pantalla

if __name__ == '__main__':
    GymApp().run()
