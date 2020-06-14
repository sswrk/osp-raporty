from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.lang import Builder
from json import dumps
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os.path
import json
import ConnectionInfo
from ReportLabel import ReportLabel

from android.permissions import request_permissions, Permission
request_permissions([Permission.INTERNET,
		     Permission.ACCESS_NETWORK_STATE,
		     Permission.WRITE_EXTERNAL_STORAGE,
                     Permission.READ_EXTERNAL_STORAGE])

def override_where():
    return os.path.abspath("certifi/cacert.pem")

import certifi


os.environ["REQUESTS_CA_BUNDLE"] = override_where()
certifi.core.where = override_where

import requests


requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()


with open('loginscreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())
with open('registerscreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())
with open('startscreen.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

from StartScreen import StartScreen
from LoginScreen import LoginScreen
from RegisterScreen import RegisterScreen


class FirebaseAuth(Screen, EventDispatcher):
    auth_key = StringProperty()

    refresh_token = ""
    logged_in = BooleanProperty(False)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.refresh_token_file = App.get_running_app().user_data_dir + "/refresh_token.txt"
        if os.path.exists(self.refresh_token_file):
            self.reload_user()

    def on_auth_key(self, *args):
        if os.path.exists(self.refresh_token_file):
            self.reload_user()

    def sign_up(self, email, password):
        url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.auth_key
        payload = {"email": email, "password": password, "returnSecureToken": "true"}
        result = requests.post(url, json=payload)
        json_result = result.json()
        if result.ok:
            self.login_success(json_result)
        else:
            self.login_failure(json_result)

    def login_success(self, log_in_data):
        self.refresh_token = log_in_data['refreshToken']
        ConnectionInfo.uid = log_in_data['localId']
        with open(self.refresh_token_file, "w") as f:
            f.write(self.refresh_token)
        self.logged_in = True
        self.load_reports()

    def login_failure(self, failure_data):
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        pop = Popup(title='Nie udało się',
                    content=Label(text=msg),
                    size_hint=(None, None), size=(400, 400))
        pop.open()

    def sign_in(self, email, password):
        url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.auth_key
        payload = {"email": email, "password": password, "returnSecureToken": True}
        result = requests.post(url, json=payload)
        json_result = result.json()
        if result.ok:
            self.login_success(json_result)
        else:
            self.login_failure(json_result)

    def reset_password(self, email):
        url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key=" + self.auth_key
        payload = {"email": email, "requestType": "PASSWORD_RESET"}
        result = requests.post(url, json=payload)
        json_result = result.json()
        if result.ok:
            self.reset_success()
        else:
            self.login_failure(json_result)

    def reset_success(self):
        msg = "Wysłano e-mail z dalszymi instrukcjami"
        pop = Popup(title='Reset hasła',
                    content=Label(text=msg),
                    size_hint=(None, None), size=(400, 400))
        pop.open()

    def reload_user(self):
        with open(self.refresh_token_file, "r") as f:
            self.refresh_token = f.read()
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.auth_key
        refresh_payload = dumps({"grant_type": "refresh_token", "refresh_token": self.refresh_token})
        UrlRequest(refresh_url, req_body=refresh_payload,
                   on_success=self.user_reload_success,
                   ca_file=certifi.where(), verify=True)

    def user_reload_success(self, url, loaded_data):
        ConnectionInfo.uid = loaded_data['user_id']
        self.logged_in = True
        self.load_reports()

    def sign_out(self):
        with open(self.refresh_token_file, 'w') as rf:
            rf.write("")
        self.logged_in = False

    def load_reports(self):
        url = ConnectionInfo.database_url + ConnectionInfo.uid + '/.json'
        ConnectionInfo.reports = json.loads(requests.get(url + '?auth=' + ConnectionInfo.database_auth_key).content)
        self.parent.ids['report_list'].ids['reports_list_grid'].clear_widgets()
        if ConnectionInfo.reports:
            for report in ConnectionInfo.reports:
                label = ReportLabel(report=report)
                grid = self.parent.ids['report_list'].ids['reports_list_grid']
                grid.add_widget(label, len(grid.children))
