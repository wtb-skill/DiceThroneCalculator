# screens/base_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

class BaseScreen(Screen):
    def create_button(self, text=None, image=None, **kwargs):
        """
        Create a Button with automatic press/release visual feedback.
        Pass size_hint_x / size_hint_y or size through kwargs to control scaling.
        """
        if image:
            btn = Button(
                background_normal=image,
                background_down=image,
                **kwargs
            )
        else:
            btn = Button(
                text=text,
                **kwargs
            )

        # Bind state to handle opacity
        btn.bind(state=self._button_state_opacity)
        return btn

    def _button_state_opacity(self, instance, value):
        """
        Automatically called whenever button state changes.
        value == 'down' → pressed
        value == 'normal' → released (even outside)
        """
        if value == "down":
            instance.opacity = 0.6
        else:
            instance.opacity = 1.0
