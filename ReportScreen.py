from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from datetime import date
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os

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
    #android:
    folder = '/storage/emulated/0/'
    #windows-demo:
    #folder = ''

    def __init__(self, **kwargs):
        self.currentdate = date.today().strftime("%d.%m.%Y")
        self.currenttime = datetime.now().strftime("%H:%M")
        super(Screen, self).__init__(**kwargs)

    def generatePDF(self):
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
        result = open(os.path.join(self.folder,'raport.pdf'), "w+b")
        result_html = open(os.path.join(self.folder,'raport.html'), "w", encoding='utf-8')
        result_html.write(html_out)
        pisa.CreatePDF(html_out.encode('utf-8'), path='__dummy__', dest=result, encoding='utf-8')
        result.close()
