from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from datetime import date
from datetime import datetime

with open('ReportScreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

class ReportScreen(Screen):
    currentdate = StringProperty()
    currenttime = StringProperty()
    def __init__(self, **kwargs):
        self.currentdate = date.today().strftime("%d.%m.%Y")
        self.currenttime = datetime.now().strftime("%H:%M")
        super(Screen, self).__init__(**kwargs)