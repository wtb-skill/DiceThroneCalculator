from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from data.characters import CHARACTERS

class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = GridLayout(cols=2, spacing=20, padding=20)

        for char_name in CHARACTERS.keys():
            btn = Button(text=char_name, font_size=24)
            btn.bind(on_press=self.select_character)
            layout.add_widget(btn)

        self.add_widget(layout)

    def select_character(self, instance):
        selected_char = instance.text
        # Pass the selected character to the AbilityDiceScreen
        ability_screen = self.manager.get_screen('ability_dice')
        ability_screen.set_character(selected_char)
        self.manager.current = 'ability_dice'
