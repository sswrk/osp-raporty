import json
import requests
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
import ConnectionInfo
from kivy.uix.popup import Popup

with open('reportlabel.kv', encoding='utf8') as f:
    Builder.load_string(f.read())


class ConfirmPopup(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


class ReportLabel(GridLayout):
    name = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(rows=1, cols=2)
        self.report = kwargs['report']
        self.name = str(self.report).replace('_', ' ').replace('-', '.')

    def show_delete_popup(self):
        content = ConfirmPopup(text='Czy na pewno chcesz usunąć raport?')
        content.bind(on_answer=self.delete_report)
        self.popup = Popup(title="Uwaga!",
                           content=content,
                           size_hint=(None, None),
                           size=(480, 400),
                           auto_dismiss=False)
        self.popup.open()

    def delete_report(self, instance, answer):
        if answer == 'yes':
            requests.delete(url=ConnectionInfo.database_url + "/" + ConnectionInfo.uid + "/" + str(self.report) + ".json")
            self.parent.remove_widget(self)
        self.popup.dismiss()
