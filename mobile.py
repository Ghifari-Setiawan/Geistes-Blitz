# Import statements (keep at the top)
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

# Set window size at the start
Window.size = (1280, 720)

# Classes for custom widgets like ImageButton
class ImageButton(ButtonBehavior, Image):
    pass

# Base screen with shared functionalities for background and layout management
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

# Main menu screen
class MainMenu(BaseScreen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        layout = FloatLayout()

        # Add the title image (at the top)
        title_image = Image(source='assets/titleimg.png', size_hint=(0.6, 0.6), pos_hint={'center_x': 0.5, 'top': 1})
        layout.add_widget(title_image)

        # Add buttons
        start_button = Button(text="Start", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        instructions_button = Button(text="How To Play", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.25})

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

# Player selection screen
class PlayerSelection(BaseScreen):
    def __init__(self, **kwargs):
        super(PlayerSelection, self).__init__(**kwargs)

        layout = FloatLayout()

        # Add the 'Select Player' image at the top
        select_player_image = Image(source='assets/selectplayer.png', size_hint=(0.6, 0.6), pos_hint={'center_x': 0.5, 'top': 1.05})
        layout.add_widget(select_player_image)

        # Add buttons for player selection (2 to 4 players)
        two_players_button = Button(text="2 Players", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.45})
        three_players_button = Button(text="3 Players", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.35})
        four_players_button = Button(text="4 Players", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.25})

        two_players_button.bind(on_press=lambda x: self.start_game(2))
        three_players_button.bind(on_press=lambda x: self.start_game(3))
        four_players_button.bind(on_press=lambda x: self.start_game(4))

        layout.add_widget(two_players_button)
        layout.add_widget(three_players_button)
        layout.add_widget(four_players_button)

        self.add_widget(layout)

    def start_game(self, num_players):
        game_screen = self.manager.get_screen('game_screen')
        game_screen.num_players = num_players
        game_screen.update_player_labels_and_scores()
        self.manager.current = 'game_screen'


class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.num_players = 4  # Default to 4 players
        self.current_card_index = 0
        self.player_turn = 0
        self.scores = [0] * self.num_players
        self.cards = ['assets/level1/card1.jpg', 'assets/level1/card2.jpg', 'assets/level1/card3.jpg']
        self.create_game_layout()

    def create_game_layout(self):
        self.layout = FloatLayout()

        # Add player labels and scores (adjusted position)
        self.player_labels = []
        self.score_labels = []
        self.selection_buttons = []

        # Add the player labels and score labels
        for i in range(4):
            player_label = Label(text=f"Player {i+1}", size_hint=(None, None), font_size=24, pos_hint=self.get_player_position(i))
            score_label = Label(text=f"Score: {self.scores[i]}", size_hint=(None, None), font_size=18, pos_hint=self.get_player_score_position(i))

            self.player_labels.append(player_label)
            self.score_labels.append(score_label)
            self.layout.add_widget(player_label)
            self.layout.add_widget(score_label)

        # Center card
        self.card_image = Image(source=self.cards[self.current_card_index], size_hint=(
            0.25, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.55})
        self.layout.add_widget(self.card_image)

        # Add selection buttons (ensure 5 items for all players)
        self.add_selection_buttons(self.layout)

        # Exit button as an icon
        exit_button = ImageButton(source='assets/exit_icon_button.png', size_hint=(
            None, None), size=(64, 64), pos_hint={'center_x': 0.5, 'top': 0.375})
        exit_button.bind(on_press=self.show_exit_popup)
        self.layout.add_widget(exit_button)

        self.add_widget(self.layout)

    def get_player_position(self, player_index):
        """
        Calculate player label positions based on player index.
        This example arranges 4 players in a cross-like pattern (top, bottom, left, right).
        """
        if self.num_players == 2:
            positions = [{'center_x': 0.5, 'top': 0.9}, {'center_x': 0.5, 'y': 0.1}]
        elif self.num_players == 3:
            positions = [{'center_x': 0.5, 'top': 0.9}, {'center_x': 0.1, 'center_y': 0.5}, {'center_x': 0.9, 'center_y': 0.5}]
        else:  # Default to 4 players
            positions = [{'center_x': 0.5, 'top': 0.9}, {'center_x': 0.1, 'center_y': 0.5}, {'center_x': 0.5, 'y': 0.1}, {'center_x': 0.9, 'center_y': 0.5}]

        return positions[player_index]

    def get_player_score_position(self, player_index):
        """
        Calculate score label positions based on player index.
        Typically, these will be placed just below the player label.
        """
        if self.num_players == 2:
            positions = [{'center_x': 0.5, 'top': 0.85}, {'center_x': 0.5, 'y': 0.15}]
        elif self.num_players == 3:
            positions = [{'center_x': 0.5, 'top': 0.85}, {'center_x': 0.1, 'center_y': 0.45}, {'center_x': 0.9, 'center_y': 0.45}]
        else:  # Default to 4 players
            positions = [{'center_x': 0.5, 'top': 0.85}, {'center_x': 0.1, 'center_y': 0.45}, {'center_x': 0.5, 'y': 0.15}, {'center_x': 0.9, 'center_y': 0.45}]

        return positions[player_index]

    def update_player_labels_and_scores(self):
        """Updates the player labels and scores based on the current number of players."""
        for i in range(4):
            if i < self.num_players:
                self.player_labels[i].text = f"Player {i+1}"
                self.player_labels[i].opacity = 1  # Make it visible
                self.score_labels[i].text = f"Score: {self.scores[i]}"
                self.score_labels[i].opacity = 1
            else:
                # Hide labels for non-existent players
                self.player_labels[i].opacity = 0
                self.score_labels[i].opacity = 0

        self.update_player_positions()

    def update_player_positions(self):
        """Repositions players dynamically based on the number of players."""
        if self.num_players == 2:
            # Player 1 at the bottom, Player 2 at the top
            self.player_labels[0].pos_hint = {'center_x': 0.5, 'y': 0.05}
            self.score_labels[0].pos_hint = {'center_x': 0.5, 'y': 0.1}
            self.player_labels[1].pos_hint = {'center_x': 0.5, 'top': 0.95}
            self.score_labels[1].pos_hint = {'center_x': 0.5, 'top': 0.9}
        elif self.num_players == 3:
            # Player 1 at the bottom, Player 2 on left, Player 3 on right
            self.player_labels[0].pos_hint = {'center_x': 0.5, 'y': 0.05}
            self.score_labels[0].pos_hint = {'center_x': 0.5, 'y': 0.1}
            self.player_labels[1].pos_hint = {'x': 0.05, 'center_y': 0.5}
            self.score_labels[1].pos_hint = {'x': 0.05, 'center_y': 0.45}
            self.player_labels[2].pos_hint = {'right': 0.95, 'center_y': 0.5}
            self.score_labels[2].pos_hint = {'right': 0.95, 'center_y': 0.45}
        else:
            # Default to 4-player positioning
            self.player_labels[0].pos_hint = {'center_x': 0.5, 'top': 0.95}
            self.score_labels[0].pos_hint = {'center_x': 0.5, 'top': 0.9}
            self.player_labels[1].pos_hint = {'x': 0.05, 'center_y': 0.5}
            self.score_labels[1].pos_hint = {'x': 0.05, 'center_y': 0.45}
            self.player_labels[2].pos_hint = {'center_x': 0.5, 'y': 0.05}
            self.score_labels[2].pos_hint = {'center_x': 0.5, 'y': 0.1}
            self.player_labels[3].pos_hint = {'right': 0.95, 'center_y': 0.5}
            self.score_labels[3].pos_hint = {'right': 0.95, 'center_y': 0.45}

    def show_exit_popup(self, instance):
        content = GridLayout(cols=2, spacing=10, padding=10)
        yes_button = Button(text="Yes", size_hint=(0.4, 0.4))
        no_button = Button(text="No", size_hint=(0.4, 0.4))

        popup = Popup(
            title="Exit Confirmation",
            content=content,
            size_hint=(0.6, 0.4)
        )

        yes_button.bind(on_press=lambda x: App.get_running_app().stop())
        no_button.bind(on_press=popup.dismiss)

        content.add_widget(yes_button)
        content.add_widget(no_button)

        popup.open()

    def add_selection_buttons(self, layout):
        self.items = ['Mouse', 'Sofa', 'Bottle', 'Book', 'Ghost']
        self.selection_buttons = []

        # Horizontal layout for Player 1 (top) and Player 2 (bottom)
        for i, item in enumerate(self.items):
            btn_top = Button(text=item, size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.3 + i * 0.1, 'top': 0.85})
            btn_bottom = Button(text=item, size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.3 + i * 0.1, 'y': 0.15})

            self.selection_buttons.append((btn_top, btn_bottom))
            layout.add_widget(btn_top)
            layout.add_widget(btn_bottom)

        # Vertical layout for Player 3 (left) and Player 4 (right)
        for i, item in enumerate(self.items):
            btn_left = Button(text=item, size_hint=(None, None), size=(100, 100), pos_hint={'x': 0.1, 'center_y': 0.75 - i * 0.15})
            btn_right = Button(text=item, size_hint=(None, None), size=(100, 100), pos_hint={'right': 0.9, 'center_y': 0.75 - i * 0.15})

            self.selection_buttons.append((btn_left, btn_right))
            layout.add_widget(btn_left)
            layout.add_widget(btn_right)

    def hide_player_items(self, player_index):
        for btn in self.selection_buttons[player_index]:
            btn.opacity = 0

    def show_player_items(self, player_index):
        for btn in self.selection_buttons[player_index]:
            btn.opacity = 1

# Build the app and screen manager
class MyGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(PlayerSelection(name='player_selection'))
        sm.add_widget(GameScreen(name='game_screen'))

        return sm

# Run the app
if __name__ == "__main__":
    MyGameApp().run()
