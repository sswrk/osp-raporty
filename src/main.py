if __name__ == "__main__":
    import ConnectionInfo

    ConnectionInfo.init()
    from kivy.app import App
    from kivy.core.window import Window

    Window.clearcolor = (0, 0.5, 1, 0)


    class MainApp(App):
        pass


    MainApp().run()
