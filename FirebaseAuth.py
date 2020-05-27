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
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
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
    web_api_key = StringProperty()

    refresh_token = ""
    localId = ""
    idToken = ""

    login_success = BooleanProperty(False)
    sign_up_msg = StringProperty()
    sign_in_msg = StringProperty()
    email_exists = BooleanProperty(False)
    email_not_found = BooleanProperty(False)

    def on_web_api_key(self, *args):
        self.refresh_token_file = App.get_running_app().user_data_dir + "/refresh_token.txt"
        if os.path.exists(self.refresh_token_file):
            self.load_saved_account()

    def sign_up(self, email, password):
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.web_api_key
        signup_payload = {"email": email, "password": password, "returnSecureToken": "true"}
        result = requests.post(signup_url, json=signup_payload)
        is_login_successful = result.ok
        json_result = result.json()
        if (is_login_successful):
            self.successful_login(signup_url, json_result)
        else:
            self.sign_up_failure(signup_url, json_result)

    def successful_login(self, urlrequest, log_in_data):
        self.refresh_token = log_in_data['refreshToken']
        ConnectionInfo.uid = log_in_data['localId']
        self.idToken = log_in_data['idToken']
        self.save_refresh_token(self.refresh_token)
        self.login_success = True
        self.load_reports()

    def sign_up_failure(self, urlrequest, failure_data):
        self.email_exists = False
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        self.sign_up_msg = msg
        if msg == "Email exists":
            self.email_exists = True
        pop = Popup(title='Nie udało się zarejestrować',
                    content=Label(text=msg),
                    size_hint=(None, None), size=(400, 400))
        pop.open()

    def sign_in(self, email, password):
        sign_in_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.web_api_key
        sign_in_payload = {"email": email, "password": password, "returnSecureToken": True}
        result = requests.post(sign_in_url, json=sign_in_payload)
        is_login_successful = result.ok
        json_result = result.json()
        if (is_login_successful):
            self.successful_login(sign_in_url, json_result)
        else:
            self.sign_in_failure(sign_in_url, json_result)

    def sign_in_failure(self, urlrequest, failure_data):
        self.email_not_found = False
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        self.sign_in_msg = msg
        if msg == "Email not found":
            self.email_not_found = True
        pop = Popup(title='Nie udało się zalogować',
                    content=Label(text=msg),
                    size_hint=(None, None), size=(400, 400))
        pop.open()

    def reset_password(self, email):
        reset_pw_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key=" + self.web_api_key
        reset_pw_data = {"email": email, "requestType": "PASSWORD_RESET"}
        result = requests.post(reset_pw_url, json=reset_pw_data)
        is_login_successful = result.ok
        json_result = result.json()
        if (is_login_successful):
            self.successful_reset(reset_pw_url, json_result)
        else:
            self.sign_in_failure(reset_pw_url, json_result)

    def successful_reset(self, urlrequest, reset_data):
        self.sign_in_msg = "Wysłano e-mail z dalszymi instrukcjami"
        pop = Popup(title='Reset hasła',
                    content=Label(text=self.sign_in_msg),
                    size_hint=(None, None), size=(400, 400))
        pop.open()

    def save_refresh_token(self, refresh_token):
        with open(self.refresh_token_file, "w") as f:
            f.write(refresh_token)

    def load_refresh_token(self):
        with open(self.refresh_token_file, "r") as f:
            self.refresh_token = f.read()

    def load_saved_account(self):
        self.load_refresh_token()
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.web_api_key
        refresh_payload = dumps({"grant_type": "refresh_token", "refresh_token": self.refresh_token})
        UrlRequest(refresh_url, req_body=refresh_payload,
                   on_success=self.successful_account_load,
                   ca_file=certifi.where(), verify=True)

    def successful_account_load(self, urlrequest, loaded_data):
        self.idToken = loaded_data['id_token']
        ConnectionInfo.uid = loaded_data['user_id']
        self.login_success = True
        self.load_reports()

    def sign_out(self):
        with open(self.refresh_token_file, 'w') as f:
            f.write("")
        self.login_success = False

    def load_reports(self):
        url = ConnectionInfo.database_url + ConnectionInfo.uid + '/.json'
        ConnectionInfo.reports = json.loads(requests.get(url + '?auth=' + ConnectionInfo.database_auth_key).content)
        self.parent.ids['report_list'].ids['reports_list_grid'].clear_widgets()
        if (ConnectionInfo.reports):
            for report in ConnectionInfo.reports:
                label = ReportLabel(report=report)
                grid = self.parent.ids['report_list'].ids['reports_list_grid']
                grid.add_widget(label, len(grid.children))
