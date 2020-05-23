import os

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout

with open('reportlistscreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

import requests
import json
import ConnectionInfo

class ReportListScreen(Screen):
    pass
