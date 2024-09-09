from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior

# Set screen dimensions
Window.size = (1280, 720)


class ImageButton(ButtonBehavior, Image):
    pass


class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            self.rect = Image(source='assets/background.jpg',
                              allow_stretch=True, keep_ratio=False)
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class MainMenu(BaseScreen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        layout = FloatLayout()

        # Add buttons
        start_button = Button(text="Start", size_hint=(
            0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        instructions_button = Button(text="How To Play", size_hint=(
            0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.35})

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
        popup = Popup(title='Instructions', content=Label(
            text=instructions_text), size_hint=(0.8, 0.6))
        popup.open()


class PlayerSelection(BaseScreen):
    def __init__(self, **kwargs):
        super(PlayerSelection, self).__init__(**kwargs)

        layout = FloatLayout()

        # Add buttons for player selection (2 to 4 players)
        two_players_button = Button(text="2 Players", size_hint=(
            0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        three_players_button = Button(text="3 Players", size_hint=(
            0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        four_players_button = Button(text="4 Players", size_hint=(
            0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.3})

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
        self.num_players = 4
        self.current_card_index = 0
        self.player_turn = 0
        self.scores = [0] * self.num_players
        self.cards = ['assets/level1/card1.jpg',
                      'assets/level1/card2.jpg', 'assets/level1/card3.jpg']
        self.create_game_layout()

    def create_game_layout(self):
        layout = FloatLayout()

        # Add player labels and scores (adjusted position)
        self.player_labels = [
            Label(text=f"Player {i+1}", size_hint=(None, None),
                  font_size=24, pos_hint=self.get_player_position(i))
            for i in range(4)
        ]
        self.score_labels = [
            Label(text=f"Score: {self.scores[i]}", size_hint=(
                None, None), font_size=18, pos_hint=self.get_player_score_position(i))
            for i in range(4)
        ]

        for i in range(4):
            layout.add_widget(self.player_labels[i])
            layout.add_widget(self.score_labels[i])

        # Center card
        self.card_image = Image(source=self.cards[self.current_card_index], size_hint=(
            0.25, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout.add_widget(self.card_image)

        # Add selection buttons
        self.add_selection_buttons(layout)

        # Exit button as an icon
        exit_button = ImageButton(source='assets/exit_icon_button.png', size_hint=(
            None, None), size=(64, 64), pos_hint={'center_x': 0.5, 'top': 0.4})
        exit_button.bind(on_press=self.show_exit_popup)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def show_exit_popup(self, instance):
        content = GridLayout(cols=2, spacing=10, padding=10)
        yes_button = Button(text="Yes", size_hint=(0.4, 0.4))
        no_button = Button(text="No", size_hint=(0.4, 0.4))

        popup = Popup(
            title="Exit Confirmation",
            content=content,
            size_hint=(0.6, 0.4)
        )

        yes_button.bind(on_press=self.exit_game)
        no_button.bind(on_press=popup.dismiss)

        content.add_widget(Label(text="Quit Game?"))
        content.add_widget(Label())  # Empty space
        content.add_widget(yes_button)
        content.add_widget(no_button)

        popup.open()

    def exit_game(self, instance):
        App.get_running_app().stop()

    def get_player_position(self, player_index):
        """Returns pos_hint for player labels around the screen based on player index."""
        positions = [
            {'center_x': 0.5, 'top': 1},   # Top (Player 1)
            {'x': 0, 'center_y': 0.5},     # Left (Player 2)
            {'center_x': 0.5, 'y': 0},     # Bottom (Player 3)
            {'right': 1, 'center_y': 0.5}  # Right (Player 4)
        ]
        return positions[player_index]

    def get_player_score_position(self, player_index):
        """Returns pos_hint for player score next to their label."""
        score_positions = [
            {'center_x': 0.5, 'top': 0.95},   # Top (Player 1)
            {'x': 0.02, 'center_y': 0.45},     # Left (Player 2)
            {'center_x': 0.5, 'y': 0.05},     # Bottom (Player 3)
            {'right': 0.98, 'center_y': 0.45}  # Right (Player 4)
        ]
        return score_positions[player_index]

    def add_selection_buttons(self, layout):
        items = ['Mouse', 'Sofa', 'Bottle', 'Book', 'Ghost']

        # Horizontal layout for Player 1 (top) and Player 3 (bottom)
        for i, item in enumerate(items):
            btn_top = Button(text=item, size_hint=(None, None), size=(
                100, 100), pos_hint={'center_x': 0.3 + i * 0.1, 'top': 0.85})
            btn_bottom = Button(text=item, size_hint=(None, None), size=(
                100, 100), pos_hint={'center_x': 0.3 + i * 0.1, 'y': 0.15})
            layout.add_widget(btn_top)
            layout.add_widget(btn_bottom)

        # Vertical layout for Player 2 (left) and Player 4 (right)
        for i, item in enumerate(items):
            btn_left = Button(text=item, size_hint=(None, None), size=(
                100, 100), pos_hint={'x': 0.1, 'center_y': 0.75 - i * 0.15})
            btn_right = Button(text=item, size_hint=(None, None), size=(
                100, 100), pos_hint={'right': 0.9, 'center_y': 0.75 - i * 0.15})
            layout.add_widget(btn_left)
            layout.add_widget(btn_right)

    def next_turn(self):
        self.player_turn = (self.player_turn + 1) % self.num_players


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(PlayerSelection(name='player_selection'))
        sm.add_widget(GameScreen(name='game_screen'))
        return sm


if __name__ == '__main__':
    MyApp().run()
