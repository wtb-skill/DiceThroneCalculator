from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from data.characters import CHARACTERS
from logic.queries.advisor_wrapper import AdvisorLogic
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
import os


class AbilityDiceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._suppress_dice_events = False

        # Main layout inside the Screen
        main_layout = BoxLayout(orientation='horizontal')

        # ----- Left Column: Abilities -----
        self.left_col = BoxLayout(orientation='vertical', size_hint_x=0.3)

        # Back button at top
        self.back_btn = Button(text="Back")
        self.back_btn.size_hint_y = None
        self.back_btn.height = 50
        self.back_btn.bind(on_press=self.go_back_to_character_selection)
        self.left_col.add_widget(self.back_btn)

        # Scrollable abilities list
        self.scroll = ScrollView()
        self.ability_layout = GridLayout(cols=1, size_hint_y=None)
        self.ability_layout.bind(minimum_height=self.ability_layout.setter('height'))
        self.scroll.add_widget(self.ability_layout)
        self.left_col.add_widget(self.scroll)
        self.ability_checks = {}

        # ----- Right Column: background image + foreground UI -----
        self.right_col = FloatLayout(size_hint_x=0.7)

        # Character background image
        self.char_image = Image(
            allow_stretch=True,  # allows scaling
            keep_ratio=False,  # disables maintaining aspect ratio so it fills container
            size_hint=(1, 1),  # take full width and height of right_col
            pos_hint={'x': 0, 'y': 0}  # position at bottom-left corner
        )
        self.right_col.add_widget(self.char_image, index=0)  # add at bottom so other widgets are on top

        # Foreground UI container inside right column (anchored at bottom)
        self.foreground_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.8, None),
            height=250,
            spacing=10,
            pos_hint={'center_x': 0.5, 'y': 0}  # Anchored at bottom now
        )

        # Dice input layout
        self.dice_layout = BoxLayout(orientation='horizontal', spacing=5)
        self.dice_inputs = []
        for _ in range(5):
            ti = TextInput(
                multiline=False,
                input_filter='int',
                halign='center',
                font_size=32,
                text_validate_unfocus=False
            )
            ti.bind(size=lambda inst, val: setattr(inst, 'padding_y', [(inst.height - inst.line_height) / 2]))
            self.dice_inputs.append(ti)
            self.dice_layout.add_widget(ti)

        # Bind text events
        for i, ti in enumerate(self.dice_inputs):
            ti.bind(text=lambda instance, value, idx=i: self.on_dice_text(instance, value, idx))

        self.foreground_layout.add_widget(self.dice_layout)

        # Results label
        self.result_label = Label(text="Results will appear here")
        self.foreground_layout.add_widget(self.result_label)

        # Analyze button
        self.analyze_btn = Button(text="Analyze")
        self.analyze_btn.bind(on_press=self.analyze_roll)
        self.foreground_layout.add_widget(self.analyze_btn)

        # Add foreground layout to right column
        self.right_col.add_widget(self.foreground_layout)

        # Add columns to main layout
        main_layout.add_widget(self.left_col)
        main_layout.add_widget(self.right_col)

        # Add main layout to the Screen
        self.add_widget(main_layout)

    # ---------------- Methods ----------------
    def on_enter(self, *args):
        Clock.schedule_once(self._focus_first_input, 0)

    def go_back_to_character_selection(self, instance):
        for cb in self.ability_checks.values():
            cb.active = False
        self.ability_checks.clear()

        for ti in self.dice_inputs:
            ti.text = ""

        self.result_label.text = "Results will appear here"
        self.char_image.source = ""  # clear image

        self.manager.current = 'character_selection'
        self.character_name = None
        self.character = None

    def set_character(self, char_name):
        if char_name not in CHARACTERS:
            self.result_label.text = f"Character {char_name} not found"
            return

        self.character_name = char_name
        self.character = CHARACTERS[char_name]

        # Load abilities
        self.load_abilities()

        # Update character image
        img_filename = f"{char_name}_full.jpg"
        img_path = os.path.join("images", "full_versions", img_filename)
        if os.path.exists(img_path):
            self.char_image.source = img_path
        else:
            self.char_image.source = ""

    def load_abilities(self):
        self.ability_checks.clear()
        self.ability_layout.clear_widgets()

        for ability_name in self.character['abilities'].MAP.keys():
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            cb = CheckBox()
            row.add_widget(cb)
            row.add_widget(Label(text=ability_name))
            self.ability_layout.add_widget(row)
            self.ability_checks[ability_name] = cb

    def analyze_roll(self, instance):
        roll = []
        for ti in self.dice_inputs:
            try:
                val = int(ti.text)
                if val < 1 or val > 6:
                    raise ValueError
                roll.append(val)
            except ValueError:
                self.result_label.text = "Enter valid dice (1-6) for all dice"
                return

        selected = [name for name, cb in self.ability_checks.items() if cb.active]
        if not selected:
            self.result_label.text = "Select at least one ability"
            return

        keep, prob = AdvisorLogic.compute_best_keep(roll, selected)
        self.result_label.text = f"Best Keep: {keep}\nProbability: {prob:.2%}"

        self._suppress_dice_events = True
        for ti in self.dice_inputs:
            ti.text = ""
        self._suppress_dice_events = False

        Clock.schedule_once(lambda dt: self._focus_first_input(), 0.2)

    def _focus_first_input(self, *args):
        for ti in self.dice_inputs:
            ti.focus = False
        if self.dice_inputs:
            self.dice_inputs[0].focus = True

    def on_dice_text(self, instance, value, idx):
        if getattr(self, "_suppress_dice_events", False):
            return

        if len(value) > 1:
            instance.text = value[-1]
            value = instance.text

        if not value.isdigit() or not (1 <= int(value) <= 6):
            instance.text = ""
            return

        if idx + 1 < len(self.dice_inputs):
            self.dice_inputs[idx + 1].focus = True
        else:
            instance.focus = False
