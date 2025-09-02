from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from data.characters import CHARACTERS
import os
from logic.commands.close_app import close_app

class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = BoxLayout(orientation='vertical', spacing=0, padding=0)

        images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')

        # ---------------- Top: Logo with Exit Image Button ----------------
        top_layout = FloatLayout(size_hint_y=0.5)  # Top half of screen

        # Logo image
        logo_file = os.path.join(images_path, 'logo.png')
        if not os.path.exists(logo_file):
            print(f"Warning: logo not found: {logo_file}")
            logo = Button(text='Logo Missing')
        else:
            logo = Image(
                source=logo_file,
                allow_stretch=True,
                keep_ratio=False,
                size_hint=(1, 1),
                pos_hint={'x': 0, 'y': 0}
            )
        top_layout.add_widget(logo)

        # Exit button as image
        close_file = os.path.join(images_path, 'close_image.png')
        if not os.path.exists(close_file):
            print(f"Warning: close image not found: {close_file}")
            exit_btn = Button(text='X', size_hint=(None, None), size=(60, 60), pos_hint={'right': 1, 'top': 1})
        else:
            exit_btn = Button(
                background_normal=close_file,
                background_down=close_file,
                size_hint=(None, None),
                size=(60, 60),
                pos_hint={'right': 1, 'top': 1},
                border=(0, 0, 0, 0)  # remove default Kivy button borders
            )
        exit_btn.bind(on_press=lambda instance: close_app())
        top_layout.add_widget(exit_btn)

        # ---------------- Bottom: Character buttons ----------------
        buttons_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)
        buttons_layout.size_hint_y = 0.5  # Bottom half of screen

        for char_name in CHARACTERS.keys():
            image_file = os.path.join(images_path, f"{char_name.lower().replace(' ', '_')}.jpg")
            btn_text = '' if os.path.exists(image_file) else char_name
            btn = Button(
                text=btn_text,
                font_size=24,
                size_hint_x=1 / len(CHARACTERS),
                background_normal=image_file if os.path.exists(image_file) else '',
                background_down=image_file if os.path.exists(image_file) else ''
            )

            btn.bind(on_press=self.select_character)
            buttons_layout.add_widget(btn)

        # Add layouts to root
        root_layout.add_widget(top_layout)
        root_layout.add_widget(buttons_layout)

        self.add_widget(root_layout)

    def select_character(self, instance):
        selected_char = instance.text if instance.text else next(
            name for name in CHARACTERS if name.lower().replace(' ', '_') in instance.background_normal
        )
        ability_screen = self.manager.get_screen('ability_dice')
        ability_screen.set_character(selected_char)
        self.manager.current = 'ability_dice'

