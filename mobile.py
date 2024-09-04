from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label

# Set screen dimensions
from kivy.core.window import Window
Window.size = (1280, 720)

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            self.rect = Image(source='assets/background.jpg', allow_stretch=True, keep_ratio=False)
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class MainMenu(BaseScreen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        layout = FloatLayout()

        # Add buttons
        start_button = Button(text="Start", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        instructions_button = Button(text="How To Play", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.35})

        start_button.bind(on_press=self.start_game)
        instructions_button.bind(on_press=self.show_instructions)

        layout.add_widget(start_button)
        layout.add_widget(instructions_button)

        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'player_selection'

    def show_instructions(self, instance):
        instructions_text = (
            "How to Play:\n"
            "1. Select the number of players.\n"
            "2. A card will be shown in the center.\n"
            "3. Players take turns selecting the correct item.\n"
            "4. Correct choices earn points, wrong choices do not.\n"
            "5. The game ends when all cards are used."
        )
        popup = Popup(title='Instructions', content=Label(text=instructions_text), size_hint=(0.8, 0.6))
        popup.open()

class PlayerSelection(BaseScreen):
    def __init__(self, **kwargs):
        super(PlayerSelection, self).__init__(**kwargs)

        layout = FloatLayout()

        # Add buttons for player selection (2 to 4 players)
        two_players_button = Button(text="2 Players", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        three_players_button = Button(text="3 Players", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        four_players_button = Button(text="4 Players", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.3})

        two_players_button.bind(on_press=lambda x: self.start_game(2))
        three_players_button.bind(on_press=lambda x: self.start_game(3))
        four_players_button.bind(on_press=lambda x: self.start_game(4))

        layout.add_widget(two_players_button)
        layout.add_widget(three_players_button)
        layout.add_widget(four_players_button)

        self.add_widget(layout)

    def start_game(self, num_players):
        self.manager.get_screen('game_screen').num_players = num_players
        self.manager.current = 'game_screen'

class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.num_players = 2  # Default value

    def on_enter(self):
        # Logic to start the game with the selected number of players
        print(f"Starting game with {self.num_players} players")
        # Here, you would add the code for the actual game logic, similar to what you had in the Pygame version

class GeistesBlitzApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(PlayerSelection(name='player_selection'))
        sm.add_widget(GameScreen(name='game_screen'))
        return sm

if __name__ == '__main__':
    GeistesBlitzApp().run()
