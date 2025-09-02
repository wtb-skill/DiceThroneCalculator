from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from data.characters import CHARACTERS
import os

class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = BoxLayout(orientation='vertical', spacing=0, padding=0)

        images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')

        # ---------------- Top: Logo ----------------
        logo_file = os.path.join(images_path, 'logo.png')
        if not os.path.exists(logo_file):
            print(f"Warning: logo not found: {logo_file}")
            logo = Button(text='Logo Missing')
        else:
            logo = Image(source=logo_file, allow_stretch=True, keep_ratio=False)

        logo_layout = BoxLayout(size_hint_y=0.5)  # Top half of vertical space
        logo_layout.add_widget(logo)

        # ---------------- Bottom: Character buttons ----------------
        buttons_layout = BoxLayout(orientation='horizontal')  # Kivy horizontal = visually vertical
        buttons_layout.size_hint_y = 0.5  # Bottom half

        for char_name in CHARACTERS.keys():
            image_file = os.path.join(images_path, f"{char_name.lower().replace(' ', '_')}.jpg")
            btn_text = '' if os.path.exists(image_file) else char_name
            btn = Button(
                text=btn_text,
                font_size=24,
                background_normal=image_file if os.path.exists(image_file) else '',
                background_down=image_file if os.path.exists(image_file) else ''
            )
            btn.bind(on_press=self.select_character)
            buttons_layout.add_widget(btn)

        # Add both layouts to root
        root_layout.add_widget(logo_layout)
        root_layout.add_widget(buttons_layout)

        self.add_widget(root_layout)

    def select_character(self, instance):
        selected_char = instance.text if instance.text else next(
            name for name in CHARACTERS if name.lower().replace(' ', '_') in instance.background_normal
        )
        ability_screen = self.manager.get_screen('ability_dice')
        ability_screen.set_character(selected_char)
        self.manager.current = 'ability_dice'
