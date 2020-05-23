from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import ConnectionInfo
import requests
import json
from ReportLabel import ReportLabel

with open('mainmenu.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

class MainMenu(Screen):
    def load_reports(self):
        url = 'https://osp-raporty.firebaseio.com/' + ConnectionInfo.uid + '/.json'
        auth_key = '4jxwy5QOS3fItV8i69hEH15yRdBas0ps6oKNecFy'
        ConnectionInfo.reports = json.loads(requests.get(url + '?auth=' + auth_key).content)
        self.parent.ids['report_list'].ids['reports_list_grid'].clear_widgets()
        if(ConnectionInfo.reports):
            for report in ConnectionInfo.reports:
                label = ReportLabel(report=report)
                grid = self.parent.ids['report_list'].ids['reports_list_grid']
                grid.add_widget(label, len(grid.children))