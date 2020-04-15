import kivy
kivy.require('1.1.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
Window.clearcolor = (0, 0.5, 1, 0)

with open('main.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

class MainMenu(Screen):
    pass

class ReportScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MainMenu(name='menu'))
sm.add_widget(ReportScreen(name='report'))

class MainApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    MainApp().run()
