from kivy.app import App
from screens.screen_manager import create_screen_manager

class DiceThroneApp(App):
    def build(self):
        return create_screen_manager()


if __name__ == "__main__":
    DiceThroneApp().run()
