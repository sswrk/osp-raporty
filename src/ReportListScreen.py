from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

with open('reportlistscreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())


class ReportListScreen(Screen):
    pass
