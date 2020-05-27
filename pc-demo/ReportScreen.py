import json
import requests
import string
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from datetime import date
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os
import ConnectionInfo
from ReportLabel import ReportLabel

with open('reportscreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())


class ReportScreen(Screen):
    currentdate = StringProperty()
    currenttime = StringProperty()

    description = ""
    lp = ""
    departure_time = ""
    departure_date = ""
    arrived = ""
    incident_place = ""
    incident_type = ""
    section_commander = ""
    action_commander = ""
    driver = ""
    causedby = ""
    victim = ""
    section = ""
    details = ""
    return_date = ""
    ended_time = ""
    return_time = ""
    meter_reading = ""
    km_to_incident_place = ""
    font = os.path.abspath("resources/Arial.ttf")
    # android:
    # folder = '/storage/emulated/0/'
    # pc:
    folder = ''

    def set_args(self, report):
        self.ids['lp'].text = ConnectionInfo.reports[report]['lp']
        self.ids['departure_time'].text = ConnectionInfo.reports[report]['departure_time']
        self.ids['departure_date'].text = ConnectionInfo.reports[report]['departure_date']
        self.ids['arrived'].text = ConnectionInfo.reports[report]['arrived']
        self.ids['incident_place'].text = ConnectionInfo.reports[report]['incident_place']
        self.ids['incident_type'].text = ConnectionInfo.reports[report]['incident_type']
        self.ids['section_commander'].text = ConnectionInfo.reports[report]['section_commander']
        self.ids['action_commander'].text = ConnectionInfo.reports[report]['action_commander']
        self.ids['driver'].text = ConnectionInfo.reports[report]['driver']
        self.ids['causedby'].text = ConnectionInfo.reports[report]['causedby']
        self.ids['victim'].text = ConnectionInfo.reports[report]['victim']
        self.ids['section'].text = ConnectionInfo.reports[report]['section']
        self.ids['details'].text = ConnectionInfo.reports[report]['details']
        self.ids['return_date'].text = ConnectionInfo.reports[report]['return_date']
        self.ids['ended_time'].text = ConnectionInfo.reports[report]['ended_time']
        self.ids['return_time'].text = ConnectionInfo.reports[report]['return_time']
        self.ids['km_to_incident_place'].text = ConnectionInfo.reports[report]['km_to_incident_place']

    def __init__(self, **kwargs):
        self.currentdate = date.today().strftime("%d.%m.%Y")
        self.currenttime = datetime.now().strftime("%H:%M")
        super(Screen, self).__init__(**kwargs)

    def add_to_database(self):
        url = 'https://osp-raporty.firebaseio.com/' + ConnectionInfo.uid + '/.json'
        report_name = ('Raport_' + self.departure_date + '_' + self.return_time + '_' + self.lp).replace('.',
                                                                                                         '-').replace(
            ':', '-')
        payload = {report_name: {"description": self.description,
                                 "lp": self.lp,
                                 "departure_date": self.departure_date,
                                 "departure_time": self.departure_time,
                                 "arrived": self.arrived,
                                 "incident_place": self.incident_place,
                                 "incident_type": self.incident_type,
                                 "section_commander": self.section_commander,
                                 "action_commander": self.action_commander,
                                 "driver": self.driver,
                                 "causedby": self.causedby,
                                 "victim": self.victim,
                                 "section": self.section,
                                 "details": self.details,
                                 "return_date": self.return_date,
                                 "ended_time": self.ended_time,
                                 "return_time": self.return_time,
                                 "meter_reading": self.meter_reading,
                                 "km_to_incident_place": self.km_to_incident_place}}
        requests.patch(url=url, json=payload)

    def generate_pdf(self):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("resources/template.html")
        template_vars = {"font": self.font,
                         "description": self.description,
                         "lp": self.lp,
                         "departure_date": self.departure_date,
                         "departure_time": self.departure_time,
                         "arrived": self.arrived,
                         "incident_place": self.incident_place,
                         "incident_type": self.incident_type,
                         "section_commander": self.section_commander,
                         "action_commander": self.action_commander,
                         "driver": self.driver,
                         "causedby": self.causedby,
                         "victim": self.victim,
                         "section": self.section,
                         "details": self.details,
                         "return_date": self.return_date,
                         "ended_time": self.ended_time,
                         "return_time": self.return_time,
                         "meter_reading": self.meter_reading,
                         "km_to_incident_place": self.km_to_incident_place}

        html_out = template.render(template_vars)
        result = open(os.path.join(self.folder,
                                   ('Raport_' + self.departure_date + '_' + self.return_time + '_' + self.lp).replace(
                                       '.', '-').replace(':', '-') + '.pdf'), "w+b")
        result_html = open(os.path.join(self.folder, (
                'Raport_' + self.departure_date + '_' + self.return_time + '_' + self.lp).replace('.', '-').replace(
            ':', '-') + '.html'), "w", encoding='utf-8')
        result_html.write(html_out)
        pisa.CreatePDF(html_out.encode('utf-8'), path='__dummy__', dest=result, encoding='utf-8')
        result.close()

    def reload_reports(self):
        replace = True
        try:
            ConnectionInfo.reports[
                ('Raport_' + self.departure_date + '_' + self.return_time + '_' + self.lp).replace('.', '-').replace(
                    ':', '-')]
        except KeyError:
            replace = False
        except TypeError:
            replace = False
        url = ConnectionInfo.database_url + ConnectionInfo.uid + '/.json'
        ConnectionInfo.reports = json.loads(requests.get(url + '?auth=' + ConnectionInfo.database_auth_key).content)
        if not replace:
            self.parent.ids['report_list'].ids['reports_list_grid'].clear_widgets()
            if ConnectionInfo.reports:
                for report in ConnectionInfo.reports:
                    label = ReportLabel(report=report)
                    grid = self.parent.ids['report_list'].ids['reports_list_grid']
                    grid.add_widget(label, len(grid.children))

    def reset_report(self):
        self.ids['lp'].text = ""
        self.ids['departure_time'].text = ""
        self.ids['departure_date'].text = date.today().strftime("%d.%m.%Y")
        self.ids['arrived'].text = ""
        self.ids['incident_place'].text = ""
        self.ids['incident_type'].text = ""
        self.ids['section_commander'].text = ""
        self.ids['action_commander'].text = ""
        self.ids['driver'].text = ""
        self.ids['causedby'].text = ""
        self.ids['victim'].text = ""
        self.ids['section'].text = ""
        self.ids['details'].text = ""
        self.ids['return_date'].text = date.today().strftime("%d.%m.%Y")
        self.ids['ended_time'].text = ""
        self.ids['return_time'].text = datetime.now().strftime("%H:%M")
        self.ids['km_to_incident_place'].text = ""

    def check_validation(self):
        error = ""
        if not self.lp == "" and not self.lp.isdigit():
            error += "Liczba porządkowa musi być liczbą!\n"
        if (not self.departure_time == "" and set(self.departure_time) - set(string.digits + ':')) \
                or (not self.ended_time == "" and set(self.ended_time) - set(string.digits + ':')) \
                or (not self.return_time == "" and set(self.return_time) - set(string.digits + ':')):

            error += "Godziny powinny byc w formacie \'GG:MM\'\n"
        if (not self.departure_date == "" and set(self.departure_date) - set(string.digits + '.'))\
                or (not self.return_date == "" and set(self.return_date) - set(string.digits + '.')):
            error += "Daty powinny byc w formacie \'dd.mm.yyyy\'\n"
        if not self.km_to_incident_place == "" and not self.km_to_incident_place.isdigit():
            error += "Kilometry do miejsca zdarzenia muszą być liczbą!\n"
        if error == "":
            return True
        pop = Popup(title='Nie zapisano raportu',
                    content=Label(text=error),
                    size_hint=(None, None), size=(400, 400))
        pop.open()
        return False
