from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from data.characters import CHARACTERS
from logic.queries.advisor_wrapper import AdvisorLogic
from kivy.clock import Clock


class AbilityDiceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._suppress_dice_events = False

        # Main layout inside the Screen
        main_layout = BoxLayout(orientation='horizontal')

        # ----- Left Column: Abilities -----
        self.left_col = BoxLayout(orientation='vertical', size_hint_x=0.3)
        self.scroll = ScrollView()
        self.ability_layout = GridLayout(cols=1, size_hint_y=None)
        self.ability_layout.bind(minimum_height=self.ability_layout.setter('height'))
        self.scroll.add_widget(self.ability_layout)
        self.left_col.add_widget(self.scroll)
        self.ability_checks = {}

        # ----- Right Column -----
        self.right_col = BoxLayout(orientation='vertical', size_hint_x=0.7, spacing=10, padding=10)

        # Update back button to handle going back
        self.back_btn = Button(text="")
        self.back_btn.bind(on_press=self.go_back_to_character_selection)
        self.right_col.add_widget(self.back_btn)

        # Middle: Dice input
        self.dice_layout = BoxLayout(orientation='horizontal', spacing=5)
        self.dice_inputs = []

        if self.dice_inputs:
            self.dice_inputs[0].focus = True

        for _ in range(5):
            ti = TextInput(
                multiline=False,
                input_filter='int',
                halign='center',  # works for horizontal centering
                font_size=32,
                text_validate_unfocus=False
            )
            # Center vertically using dynamic padding_y
            ti.bind(
                size=lambda inst, val: setattr(
                    inst, 'padding_y', [(inst.height - inst.line_height) / 2]
                )
            )
            self.dice_inputs.append(ti)
            self.dice_layout.add_widget(ti)
        self.right_col.add_widget(self.dice_layout)

        # Bind for auto-switching
        for i, ti in enumerate(self.dice_inputs):
            # Limit to one character (1-6)
            ti.bind(text=lambda instance, value, idx=i: self.on_dice_text(instance, value, idx))

        # <-- Set focus on first dice input here, after creating all of them
        if self.dice_inputs:
            self.dice_inputs[0].focus = True

        # Results display
        self.result_label = Label(text="Results will appear here")
        self.right_col.add_widget(self.result_label)

        # Analyze button
        self.analyze_btn = Button(text="Analyze")
        self.analyze_btn.bind(on_press=self.analyze_roll)
        self.right_col.add_widget(self.analyze_btn)

        # Add columns to main layout
        main_layout.add_widget(self.left_col)
        main_layout.add_widget(self.right_col)

        # Add main layout to the Screen
        self.add_widget(main_layout)

    # ---------------- Methods ----------------
    def on_enter(self, *args):
        """Called whenever this screen is entered."""
        Clock.schedule_once(self._focus_first_input, 0)

    def go_back_to_character_selection(self, instance):
        """Return to character selection screen and clear current data"""
        # Clear selected abilities
        for cb in self.ability_checks.values():
            cb.active = False
        self.ability_checks.clear()

        # Clear dice inputs
        for ti in self.dice_inputs:
            ti.text = ""

        # Clear results
        self.result_label.text = "Results will appear here"

        # Switch back to character selection screen
        self.manager.current = 'character_selection'
        self.character_name = None
        self.character = None

    def set_character(self, char_name):
        """Set current character and populate abilities dynamically"""
        if char_name not in CHARACTERS:
            self.result_label.text = f"Character {char_name} not found"
            return

        self.character_name = char_name
        self.character = CHARACTERS[char_name]

        # Update back button text
        self.back_btn.text = f"Character: {char_name} (Back)"
        self.load_abilities()

    def load_abilities(self):
        """Populate checkboxes based on selected character"""
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
        """Analyze dice and selected abilities"""
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

        # Clear dice inputs
        for ti in self.dice_inputs:
            ti.text = ""

        # Refocus first input on next frame
        Clock.schedule_once(self._focus_first_input, 0)

    def _focus_first_input(self, *args):
        # force blur others, then focus the first
        for ti in self.dice_inputs:
            ti.focus = False
        if self.dice_inputs:
            self.dice_inputs[0].focus = True

    def on_dice_text(self, instance, value, idx):
        """Automatically focus next dice input on valid number,
        enforce single-digit (1-6), and backspace to previous dice if empty.
        """
        # ignore events during programmatic clears
        if getattr(self, "_suppress_dice_events", False):
            return

        # enforce single digit
        if len(value) > 1:
            instance.text = value[-1]
            value = instance.text

        # only allow 1..6
        if not value.isdigit() or not (1 <= int(value) <= 6):
            instance.text = ""
            return

        # Move focus to next input, or remove focus if this is the last one
        if idx + 1 < len(self.dice_inputs):
            self.dice_inputs[idx + 1].focus = True
        else:
            instance.focus = False
