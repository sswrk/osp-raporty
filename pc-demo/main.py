from MainMenu import MainMenu
from ReportScreen import ReportScreen
from Login import CreateAccountWindow
from Login import LoginWindow

import kivy
kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
Window.clearcolor = (0, 0.5, 1, 0)

sm = ScreenManager()
sm.add_widget(LoginWindow(name='login'))
sm.add_widget(MainMenu(name='menu'))
sm.add_widget(ReportScreen(name='report'))
sm.add_widget(CreateAccountWindow(name='create'))

sm.current = 'login'

def getScreenManager():
    return sm

class MainApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MainApp().run()
