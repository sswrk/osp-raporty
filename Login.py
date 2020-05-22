from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

with open('login.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    surname = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def invalidForm(self):
        pop = Popup(title='Invalid Form',
                    content=Label(text='Please fill in all inputs with valid information.'),
                    size_hint=(None, None), size=(400, 400))

        pop.open()

    def submit(self):
        if self.namee.text != "" and self.surname.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                #TODO: dodawanie użytkownika do bazy

                self.reset()
                return True
            else:
                return False
        else:
            return False

    def login(self):
        self.reset()

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""
        self.surname.text = ""


class LoginWindow(Screen):

    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def invalidLogin(self):
        pop = Popup(title='Invalid Login',
                    content=Label(text='Invalid username or password.'),
                    size_hint=(None, None), size=(400, 400))
        pop.open()
        pop.open()

    def login(self):
        if(1==1): #TODO: walidacja w ifie
            self.reset()
            return True
        return False

    def createBtn(self):
        self.reset()

    def reset(self):
        self.email.text = ""
        self.password.text = ""