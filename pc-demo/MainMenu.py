from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import ConnectionInfo
import requests
import json

with open('mainmenu.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

class MainMenu(Screen):
    pass