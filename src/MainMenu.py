from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

with open('mainmenu.kv', encoding='utf8') as f:
    Builder.load_string(f.read())


class MainMenu(Screen):
    pass
