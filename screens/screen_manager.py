# screens/screen_manager.py
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from .character_selection_screen import CharacterSelectionScreen
from .ability_dice_screen import AbilityDiceScreen

def create_screen_manager():
    sm = ScreenManager(transition=SlideTransition(duration=0.4))  # transition lasts 0.4s
    sm.add_widget(CharacterSelectionScreen(name='character_selection'))
    sm.add_widget(AbilityDiceScreen(name='ability_dice'))
    return sm
