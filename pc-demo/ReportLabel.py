import json

import requests
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
import ConnectionInfo

with open('reportlabel.kv', encoding='utf8') as f:
    Builder.load_string(f.read())


class ReportLabel(GridLayout):
    name = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(rows=1, cols=2)
        self.report = kwargs['report']
        self.name = str(self.report).replace('_', ' ').replace('-', '.')
