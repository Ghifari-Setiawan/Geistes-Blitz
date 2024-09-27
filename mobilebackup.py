# Import statements (keep at the top)
from random import randint
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
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Translate
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.video import Video
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.graphics import Ellipse, Color
from kivy.uix.widget import Widget


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

        # Add Start button
        start_button = Button(
            size_hint=(0.2, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_normal='assets/start.png',  # Use your styled button image
            background_down='assets/start_button_pressed.png',
        )

        # Add How to Play button
        instructions_button = Button(
            size_hint=(0.3, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_normal='assets/howtoplay.png',  # Styled button image
            background_down='assets/howtoplay_button_pressed.png',
        )

        start_button.bind(on_press=self.start_game)
        instructions_button.bind(on_press=self.show_instructions)

        layout.add_widget(start_button)
        layout.add_widget(instructions_button)

        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'player_selection'

    def show_instructions(self, instance):
        # Create a layout for the popup
        popup_layout = FloatLayout()

        # Create the video widget and add it to the layout
        video = VideoPlayer(source='assets/placeholder.mp4', state='play', size_hint=(0.9, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        popup_layout.add_widget(video)

        # Create a close button to dismiss the popup
        close_button = Button(text="Close", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.1})
        popup_layout.add_widget(close_button)

        # Create a popup to show the video
        popup = Popup(title='How to Play', content=popup_layout, size_hint=(0.8, 0.8))
        close_button.bind(on_press=popup.dismiss)

        popup.open()

# Player selection screen
class PlayerSelection(BaseScreen):
    def __init__(self, **kwargs):
        super(PlayerSelection, self).__init__(**kwargs)

        layout = FloatLayout()

        # Add the 'Select Player' image at the top
        select_player_image = Image(source='assets/selectplayer.png', size_hint=(0.6, 0.6), pos_hint={'center_x': 0.5, 'top': 1.1})
        layout.add_widget(select_player_image)

        # Add buttons for player selection with background images
        two_players_button = Button(
            size_hint=(0.35, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            background_normal='assets/2players.png',
            background_down='assets/2player_button_pressed.png',
        )
        
        three_players_button = Button(
            size_hint=(0.35, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_normal='assets/3players.png',
            background_down='assets/3player_button_pressed.png',
        )

        four_players_button = Button(
            size_hint=(0.35, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_normal='assets/4players.png',
            background_down='assets/4player_button_pressed.png',
        )

        # Bind the button events
        two_players_button.bind(on_press=lambda x: self.start_game(2))
        three_players_button.bind(on_press=lambda x: self.start_game(3))
        four_players_button.bind(on_press=lambda x: self.start_game(4))

        # Add the buttons to the layout
        layout.add_widget(two_players_button)
        layout.add_widget(three_players_button)
        layout.add_widget(four_players_button)

        # Back button to return to the main menu
        back_button = Button(
            size_hint=(0.15, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_normal='assets/back_button.png',  # Optional back button styling
            background_down='assets/back_button_pressed.png'
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def start_game(self, num_players):
        game_screen = self.manager.get_screen('game_screen')
        game_screen.num_players = num_players
        game_screen.update_player_labels_and_scores()
        self.manager.current = 'game_screen'

    def go_back(self, instance):
        self.manager.current = 'main_menu'


    def start_game(self, num_players):
        game_screen = self.manager.get_screen('game_screen')
        game_screen.num_players = num_players
        game_screen.update_player_labels_and_scores()
        self.manager.current = 'game_screen'

def animate_card_flip(self):
    """Animates the card with rotation and floating effects, plays sound."""
    if self.current_card_index >= len(self.cards):
        return

    self.card_image.source = self.cards[self.current_card_index]

    # Create a more complex animation: rotation + scaling
    anim = Animation(scale=0, duration=0.2) + Animation(scale=1, duration=0.2) + Animation(rotation=360, duration=0.5)
    anim.start(self.card_image)

    if self.card_flip_sound:
        self.card_flip_sound.play()

    # Update card index
    self.current_card_index += 1
    self.update_card_indicator()

    # Check if it's the last card, and trigger a win if needed
    if self.current_card_index >= len(self.cards):
        self.on_player_win(self.player_turn)


def trigger_confetti_animation(self):
    for _ in range(50):  # Create multiple confetti pieces
        confetti = Confetti()
        self.layout.add_widget(confetti)
        confetti.animate()

class Confetti(Widget):
    def __init__(self, **kwargs):
        super(Confetti, self).__init__(**kwargs)
        self.image = Image(source="assets/confetti.png", size_hint=(None, None), size=(30, 30))
        self.add_widget(self.image)
        self.image.pos = (randint(0, Window.width), Window.height)  # Start from top

    def animate(self):
        # Animate the confetti falling down
        end_pos = (self.image.x, 0)
        anim = Animation(pos=end_pos, duration=2, t='out_bounce')
        anim.bind(on_complete=self.remove_confetti)
        anim.start(self.image)

    def remove_confetti(self, *args):
        # Remove confetti once it reaches the bottom
        self.parent.remove_widget(self)


class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.num_players = 4  # Default to 4 players
        self.current_card_index = 0
        self.player_turn = 0
        self.scores = [0] * self.num_players
        self.cards = ['assets/level1/card1.jpg', 'assets/level1/card2.jpg', 'assets/level1/card3.jpg']
        self.create_game_layout()
        self.card_flip_sound = SoundLoader.load('assets/card_flip.wav')  # Load sound effect
        self.success_sound = SoundLoader.load('assets/success.wav')

    def create_game_layout(self):
        self.layout = FloatLayout()

        # Add player labels and scores (adjusted position and rotation)
        self.player_labels = []
        self.score_labels = []

        rotations = [0, 90, 180, 270]

        for i in range(self.num_players):
            with self.layout.canvas:
                PushMatrix()
                Rotate(angle=rotations[i], origin=(self.width / 2, self.height / 2))  # Rotate around the center

                player_label = Label(text=f"Player {i+1}", font_size=24, pos_hint=self.get_player_position(i))
                score_label = Label(text=f"{self.scores[i]} pts", font_size=18, pos_hint=self.get_player_score_position(i))

                self.player_labels.append(player_label)
                self.score_labels.append(score_label)
                self.layout.add_widget(player_label)
                self.layout.add_widget(score_label)

                PopMatrix()

        # Add the card image
        self.card_image = Image(source=self.cards[self.current_card_index], size_hint=(0.25, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.55})
        self.layout.add_widget(self.card_image)

        # Add card indicator label
        self.cards_left_label = Label(text=f"Cards Left: {len(self.cards) - self.current_card_index}",
                                    font_size=24, pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.layout.add_widget(self.cards_left_label)

        # Add selection buttons (ensure 5 items for all players)
        self.add_selection_buttons(self.layout)

        # Exit button as an icon
        exit_button = ImageButton(source='assets/exit_icon_button.png', size_hint=(
            None, None), size=(64, 64), pos_hint={'center_x': 0.5, 'top': 0.375})
        exit_button.bind(on_press=self.show_exit_popup)
        self.layout.add_widget(exit_button)

        self.add_widget(self.layout)

    def update_card_indicator(self):
        cards_left = len(self.cards) - self.current_card_index
        self.cards_left_label.text = f"Cards Left: {cards_left}"

    def animate_card_flip(self):
        """Animates the card flip with scaling and plays sound."""
        anim = Animation(scale=0, duration=0.2) + Animation(scale=1, duration=0.2)
        anim.start(self.card_image)

        if self.card_flip_sound:
            self.card_flip_sound.play()

    def get_player_position(self, player_index):
        """Calculate player label positions."""
        positions = [{'center_x': 0.5, 'top': 0.9}, {'center_x': 0.1, 'center_y': 0.5}, 
                     {'center_x': 0.5, 'y': 0.1}, {'center_x': 0.9, 'center_y': 0.5}]
        return positions[player_index]

    def get_player_score_position(self, player_index):
        """Calculate score label positions."""
        positions = [{'center_x': 0.5, 'top': 0.85}, {'center_x': 0.1, 'center_y': 0.45}, 
                     {'center_x': 0.5, 'y': 0.15}, {'center_x': 0.9, 'center_y': 0.45}]
        return positions[player_index]

    def update_player_labels_and_scores(self):
        """Updates the player labels and scores."""
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
        """Repositions players dynamically based on the number of players and rotation."""
        layout_width, layout_height = self.layout.size  # Get the layout's size

        if self.num_players == 2:
            # Player 1 at the bottom, Player 2 at the top
            self.player_labels[0].pos = (layout_width / 2 - self.player_labels[0].width / 2, 0.1 * layout_height)
            self.score_labels[0].pos = (layout_width / 2 - self.score_labels[0].width / 2, 0.05 * layout_height)

            self.player_labels[1].pos = (layout_width / 2 - self.player_labels[1].width / 2, 0.85 * layout_height - self.player_labels[1].height)
            self.score_labels[1].pos = (layout_width / 2 - self.score_labels[1].width / 2, 0.80 * layout_height)

        elif self.num_players == 3:
            # Player 1 at the bottom, Player 2 on the left, Player 3 on the right
            self.player_labels[0].pos = (layout_width / 2 - self.player_labels[0].width / 2, 0.1 * layout_height)
            self.score_labels[0].pos = (layout_width / 2 - self.score_labels[0].width / 2, 0.05 * layout_height)

            self.player_labels[1].pos = (0.1 * layout_width, layout_height / 2 - self.player_labels[1].height / 2)
            self.score_labels[1].pos = (0.1 * layout_width, layout_height / 2 - self.score_labels[1].height / 2 - 30)

            self.player_labels[2].pos = (0.9 * layout_width - self.player_labels[2].width, layout_height / 2 - self.player_labels[2].height / 2)
            self.score_labels[2].pos = (0.9 * layout_width - self.score_labels[2].width, layout_height / 2 - self.score_labels[2].height / 2 - 30)

        else:
            # Default to 4-player positioning
            self.player_labels[0].pos = (layout_width / 2 - self.player_labels[0].width / 2, 0.01 * layout_height)
            self.score_labels[0].pos = (layout_width / 2 - self.score_labels[0].width / 2, 0.005 * layout_height)

            self.player_labels[1].pos = (0.1 * layout_width, layout_height / 2 - self.player_labels[1].height / 2)
            self.score_labels[1].pos = (0.1 * layout_width, layout_height / 2 - self.score_labels[1].height / 2 - 30)

            self.player_labels[2].pos = (layout_width / 2 - self.player_labels[2].width / 2, 0.85 * layout_height - self.player_labels[2].height)
            self.score_labels[2].pos = (layout_width / 2 - self.score_labels[2].width / 2, 0.80 * layout_height)

            self.player_labels[3].pos = (0.9 * layout_width - self.player_labels[3].width, layout_height / 2 - self.player_labels[3].height / 2)
            self.score_labels[3].pos = (0.9 * layout_width - self.score_labels[3].width, layout_height / 2 - self.score_labels[3].height / 2 - 30)

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
        self.items = ['assets/tikus.png', 'assets/sofa.png', 'assets/botol.png', 'assets/buku.png', 'assets/setan.png']
        self.selection_buttons = []

        for i, item in enumerate(self.items):
            btn_top = ImageButton(source=item, size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.3 + i * 0.1, 'top': 0.85})
            btn_bottom = ImageButton(source=item, size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.3 + i * 0.1, 'y': 0.15})

            self.selection_buttons.append((btn_top, btn_bottom))
            layout.add_widget(btn_top)
            layout.add_widget(btn_bottom)

        for i, item in enumerate(self.items):
            btn_left = ImageButton(source=item, size_hint=(None, None), size=(100, 100), pos_hint={'x': 0.1, 'center_y': 0.75 - i * 0.15})
            btn_right = ImageButton(source=item, size_hint=(None, None), size=(100, 100), pos_hint={'right': 0.9, 'center_y': 0.75 - i * 0.15})

            self.selection_buttons.append((btn_left, btn_right))
            layout.add_widget(btn_left)
            layout.add_widget(btn_right)

        self.update_selection_buttons_visibility()

    def update_selection_buttons_visibility(self):
        """Shows or hides player item buttons based on the number of players."""
        if self.num_players == 2:
            self.show_player_items(0)
            self.show_player_items(1)
            self.hide_player_items(2)
            self.hide_player_items(3)
        elif self.num_players == 3:
            self.show_player_items(0)
            self.show_player_items(1)
            self.show_player_items(2)
            self.hide_player_items(3)
        else:
            self.show_player_items(0)
            self.show_player_items(1)
            self.show_player_items(2)
            self.show_player_items(3)

    def hide_player_items(self, player_index):
        for btn in self.selection_buttons[player_index]:
            btn.opacity = 0
            btn.disabled = True

    def show_player_items(self, player_index):
        for btn in self.selection_buttons[player_index]:
            btn.opacity = 1
            btn.disabled = False

# Build the app and screen manager
class GeistesBlitz(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(PlayerSelection(name='player_selection'))
        sm.add_widget(GameScreen(name='game_screen'))

        return sm

# Run the app
if __name__ == "__main__":
    GeistesBlitz().run()
