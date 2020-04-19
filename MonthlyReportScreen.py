from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

with open('MonthlyReportScreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

class MonthlyReportScreen(Screen):
    pass