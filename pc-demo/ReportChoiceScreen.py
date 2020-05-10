from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

with open('reportchoicescreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

class ReportChoiceScreen(Screen):
    pass