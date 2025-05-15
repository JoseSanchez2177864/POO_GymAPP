# app.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from InS import InSp
from CrS import CrSp
from Inicio import Iniciop
from Entr import Entrp
from Config import Configp
from Stats import Statsp
from CRUDu import CRUDup
from CRUDp import CRUDpp
from Planes import Planesp

class GymApp(App):
    def build(self):
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

if __name__ == '__main__':
    GymApp().run()
