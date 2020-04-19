from MainMenu import MainMenu
from ReportChoiceScreen import ReportChoiceScreen
from ReportScreen import ReportScreen
from MonthlyReportScreen import MonthlyReportScreen
from YearlyReportScreen import YearlyReportScreen

import kivy
kivy.require('1.1.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
Window.clearcolor = (0, 0.5, 1, 0)

sm = ScreenManager()
sm.add_widget(MainMenu(name='menu'))
sm.add_widget(ReportChoiceScreen(name='choice'))
sm.add_widget(ReportScreen(name='report'))
sm.add_widget(MonthlyReportScreen(name='monthly'))
sm.add_widget(YearlyReportScreen(name='yearly'))

class MainApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    MainApp().run()
