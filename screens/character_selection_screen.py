from .base_screen import BaseScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from data.characters import CHARACTERS
import os
from logic.commands.close_app import close_app


class CharacterSelectionScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        root_layout = BoxLayout(orientation='vertical', spacing=0, padding=0)
        root_layout.add_widget(self.build_top_layout())
        root_layout.add_widget(self.build_bottom_layout())
        self.add_widget(root_layout)

    def build_top_layout(self):
        """Top half: logo + exit button"""
        top_layout = FloatLayout(size_hint_y=0.5)

        base_path = os.path.dirname(os.path.dirname(__file__))
        misc_path = os.path.join(base_path, 'images', 'misc')

        # Logo
        logo_file = os.path.join(misc_path, 'logo.png')
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

        # Exit button
        close_file = os.path.join(misc_path, 'close_image.png')
        if not os.path.exists(close_file):
            print(f"Warning: close image not found: {close_file}")
            exit_btn = self.create_button(
                text='X',
                size_hint=(None, None),
                size=(100, 100),
                pos_hint={'right': 1, 'top': 1}
            )
        else:
            exit_btn = self.create_button(
                image=close_file,
                size_hint=(None, None),
                size=(100, 100),
                pos_hint={'right': 1, 'top': 1}
            )
        exit_btn.bind(on_release=lambda instance: close_app())
        top_layout.add_widget(exit_btn)

        return top_layout

    def build_bottom_layout(self):
        """Bottom half: character selection buttons"""
        buttons_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0, size_hint_y=0.5)

        base_path = os.path.dirname(os.path.dirname(__file__))
        heads_path = os.path.join(base_path, 'images', 'heads')

        for char_name in CHARACTERS.keys():
            image_file = os.path.join(heads_path, f"{char_name.lower().replace(' ', '_')}.jpg")
            btn_text = '' if os.path.exists(image_file) else char_name

            btn = self.create_button(
                text=btn_text if btn_text else None,
                image=image_file if os.path.exists(image_file) else None,
                size_hint_x=1 / len(CHARACTERS),
                size_hint_y=1
            )
            btn.bind(on_release=self.select_character)
            buttons_layout.add_widget(btn)

        return buttons_layout

    def select_character(self, instance):
        if instance.text:
            selected_char = instance.text
        else:
            selected_char = next(
                name for name in CHARACTERS
                if name.lower().replace(' ', '_') in instance.background_normal
            )

        self.manager.transition.direction = 'left'  # slide left
        ability_screen = self.manager.get_screen('ability_dice')
        ability_screen.set_character(selected_char)
        self.manager.current = 'ability_dice'
