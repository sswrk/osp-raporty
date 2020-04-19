from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

with open('YearlyReportScreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

class YearlyReportScreen(Screen):
    pass