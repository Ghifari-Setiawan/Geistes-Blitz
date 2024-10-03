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
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
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
        video = VideoPlayer(source='assets/placeholder.mp4',size_hint=(0.9, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        video.state = 'play'
        video.options = {'eos': 'loop'}
        video.allow_stretch = True
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
        self.is_second_card_visible = False
        self.current_player_index = 0
        self.scores = [0] * self.num_players  # Initialize player scores
        self.cards = self.create_cards()  # Initialize the cards
        self.create_game_layout()  # Create the game layout
        self.reset_game()  # Initialize the game at the start

    def reset_game(self):
        """Resets the game state, including cards and scores."""
        self.current_card_index = 0
        self.player_turn = 0
        self.scores = [0] * self.num_players  # Reset scores
        self.cards = self.create_cards()  # Reset cards
        self.card_image_1 = None
        self.card_image_2 = None
        self.is_second_card_visible = False
        self.current_player_index = 0
        self.update_player_labels_and_scores()
        self.update_card()

    def create_game_layout(self):
        self.layout = FloatLayout()

        # Create items and cards
        self.items = self.create_items()
        self.cards = self.create_cards()
        self.current_card = self.cards[0]

        # Add player labels and scores dynamically based on num_players
        self.player_labels = []
        self.score_labels = []


        for i in range(self.num_players):
            player_label = Label(text=f"Player {i+1}", font_size=24, pos_hint=self.get_player_position(i))
            score_label = Label(text=f"{self.scores[i]} pts", font_size=18, pos_hint=self.get_player_score_position(i))

            self.player_labels.append(player_label)
            self.score_labels.append(score_label)
            self.layout.add_widget(player_label)
            self.layout.add_widget(score_label)
        
        self.update_player_labels_and_scores()  # Position the player labels and scores

        # Add first card at the center
        self.card_image_1 = self.add_card_at_position(self.cards[self.current_card_index], pos_hint={'center_x': 0.4, 'center_y': 0.50})

        # Add card indicator label (optional for showing remaining cards)
        self.cards_left_label = Label(text=f"Cards Left: {len(self.cards) - self.current_card_index}",
                                    font_size=24, pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.layout.add_widget(self.cards_left_label)

        # Add selection buttons
        self.add_selection_buttons()

        # Add an exit button below the center card
        exit_button = ImageButton(source='assets/exit_icon_button.png', size_hint=(None, None), size=(64, 64), pos_hint={'center_x': 0.5, 'center_y': 0.30})
        exit_button.bind(on_press=self.show_exit_popup)
        self.layout.add_widget(exit_button)

        self.add_widget(self.layout)

    def add_card_at_position(self, card, pos_hint):
        """Menambahkan kartu ke layar pada posisi tertentu."""
        card_image = ImageButton(source='assets/back_card.jpg', size_hint=(0.30, 0.30), pos_hint=pos_hint)
        card_image.bind(on_press=self.card_clicked)
        self.layout.add_widget(card_image)
        return card_image

    def card_clicked(self, instance):
        """Method yang dipanggil saat kartu diklik."""
        print("Kartu diklik!")

        # Panggil animasi flip kartu (optional)
        self.animate_card_flip()
        self.update_next_card()

    def update_next_card(self):
        """Moves to the next card."""
        self.current_card_index += 1
        if self.current_card_index < len(self.cards):
            if not self.is_second_card_visible:
                self.card_image_2 = self.add_card_at_position(self.cards[self.current_card_index], pos_hint={'center_x': 0.6, 'center_y': 0.50})
                self.is_second_card_visible = True
            else:
                # Jika kedua kartu sudah muncul, ganti gambar dari kedua kartu tersebut
                if self.current_card_index < len(self.cards):
                    self.card_image_2.source = self.cards[self.current_card_index]['image']
            self.cards_left_label.text = f"Cards Left: {len(self.cards) - self.current_card_index}"

        else:
            print("All cards have been used.")
            self.display_scores()

    def animate_card_flip(self):
        """Animasi flip kartu (dummy, bisa ditambahkan animasi sebenarnya)."""
        print("Animasi flip kartu berjalan...")

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
        
    def add_selection_buttons(self):
        """Creates item selection buttons for each player."""
        positions = [{'center_x': 0.53, 'center_y': 0.80},  # Player 1 (top)
                     {'center_x': 0.25, 'center_y': 0.65},  # Player 2 (left)
                     {'center_x': 0.53, 'y': 0.10},  # Player 3 (bottom)
                     {'center_x': 1.00, 'center_y': 0.65}]  # Player 4 (right)

        # For each player, create item buttons around their position
        for i in range(self.num_players):
            # Adjust item button layout based on player index
            button_layout = GridLayout(cols=5 if i % 2 == 0 else 1, size_hint=(None, None), width=400, height=100)

            for item in self.items:
                item_button = Button(background_normal=item['image'], size_hint=(None, None), size=(64, 64))
                item_button.bind(on_release=lambda btn, item=item: self.handle_item_selection(item))
                button_layout.add_widget(item_button)

            button_layout.pos_hint = positions[i]
            self.layout.add_widget(button_layout)

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
        """Repositions players dynamically based on the number of players and screen layout."""

        if self.num_players == 2:
            print("Permainan sudah dimulai dengan 2 Players!")
            # Player 1 at the bottom, Player 2 at the top
            self.player_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.130}  # Centered near the bottom
            self.score_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.090}

            self.player_labels[1].pos_hint = {'center_x': 0.5, 'center_y': 0.95}  # Centered near the top
            self.score_labels[1].pos_hint = {'center_x': 0.5, 'center_y': 0.90}

        elif self.num_players == 3:
            print("Permainan sudah dimulai dengan 3 Players!")
            # Player 1 at the bottom, Player 2 on the left, Player 3 on the right
            self.player_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.130}  # Bottom center
            self.score_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.090}

            self.player_labels[1].pos_hint = {'center_x': 0.050, 'center_y': 0.5}  # Left center
            self.score_labels[1].pos_hint = {'center_x': 0.050, 'center_y': 0.45}

            self.player_labels[2].pos_hint = {'center_x': 0.95, 'center_y': 0.5}  # Right center
            self.score_labels[2].pos_hint = {'center_x': 0.95, 'center_y': 0.45}

        else:
            print("Permainan sudah dimulai dengan 4 Players!")
            # Player 1 at the bottom, Player 2 on the left, Player 3 on the top, Player 4 on the right
            self.player_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.130}  # Bottom center
            self.score_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.090}

            self.player_labels[1].pos_hint = {'center_x': 0.050, 'center_y': 0.5}  # Left center
            self.score_labels[1].pos_hint = {'center_x': 0.050, 'center_y': 0.45}

            self.player_labels[2].pos_hint = {'center_x': 0.5, 'center_y': 0.95}  # Top center
            self.score_labels[2].pos_hint = {'center_x': 0.5, 'center_y': 0.90}

            self.player_labels[3].pos_hint = {'center_x': 0.95, 'center_y': 0.5}  # Right center
            self.score_labels[3].pos_hint = {'center_x': 0.95, 'center_y': 0.45}




    def create_items(self):
        """Defines the available items with images."""
        return [
            {'name': 'Ghost', 'image': 'assets/setan.png'},
            {'name': 'Book', 'image': 'assets/buku.png'},
            {'name': 'Bottle', 'image': 'assets/botol.png'},
            {'name': 'Mouse', 'image': 'assets/tikus.png'},
            {'name': 'Sofa', 'image': 'assets/sofa.png'},
        ]

    def create_cards(self):
        """Defines the cards, including correct and incorrect items."""
        return [
            {'image': 'assets/level1/card1.jpg', 'correct_item': 'Sofa', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card2.jpg', 'correct_item': 'Ghost', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card3.jpg', 'correct_item': 'Sofa', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card4.jpg', 'correct_item': 'Ghost', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card5.jpg', 'correct_item': 'Book', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card6.jpg', 'correct_item': 'Ghost', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card7.jpg', 'correct_item': 'Book', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card8.jpg', 'correct_item': 'Mouse', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card9.jpg', 'correct_item': 'Sofa', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card10.jpg', 'correct_item': 'Ghost', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level2/card11.jpg', 'correct_item': None, 'incorrect_item': 'Sofa', 'level': 2, 'used': False},
            {'image': 'assets/level2/card12.jpg', 'correct_item': None, 'incorrect_item': 'Bottle', 'level': 2, 'used': False},
            {'image': 'assets/level2/card13.jpg', 'correct_item': None, 'incorrect_item': 'Mouse', 'level': 2, 'used': False},
            {'image': 'assets/level2/card14.jpg', 'correct_item': None, 'incorrect_item': 'Bottle', 'level': 2, 'used': False},
            {'image': 'assets/level2/card15.jpg', 'correct_item': None, 'incorrect_item': 'Mouse', 'level': 2, 'used': False},
            {'image': 'assets/level2/card16.jpg', 'correct_item': None, 'incorrect_item': 'Book', 'level': 2, 'used': False},
            {'image': 'assets/level2/card17.jpg', 'correct_item': None, 'incorrect_item': 'Book', 'level': 2, 'used': False},
            {'image': 'assets/level2/card18.jpg', 'correct_item': None, 'incorrect_item': 'Bottle', 'level': 2, 'used': False},
            {'image': 'assets/level2/card19.jpg', 'correct_item': None, 'incorrect_item': 'Mouse', 'level': 2, 'used': False},
            {'image': 'assets/level2/card20.jpg', 'correct_item': None, 'incorrect_item': 'Bottle', 'level': 2, 'used': False},
        ]

    def handle_item_selection(self, selected_item):
        # Check current card level and validate selection
        if self.current_card['level'] == 1:
            if selected_item['name'] == self.current_card['correct_item']:
                self.scores[self.player_turn] += 1  # Increase score for current player
                print(f"Player {self.player_turn + 1} selected the correct item!")
            else:
                print(f"Player {self.player_turn + 1} selected the wrong item!")
        elif self.current_card['level'] == 2:
            if selected_item['name'] == self.current_card['incorrect_item']:
                self.scores[self.player_turn] += 1
                print(f"Player {self.player_turn + 1} selected the correct item!")
            else:
                print(f"Player {self.player_turn + 1} selected the wrong item!")

        # Move to the next card or end the game
        next_card = next((card for card in self.cards if not card['used']), None)
        
        if next_card:
            self.current_card = next_card  # Update the current card
            self.current_card['used'] = True  # Mark it as used
        else:
            print("No Cards Remaining!")
            self.display_scores()  # Display final scores when the game ends
            return

        # Move to the next player
        self.current_player_index = (self.current_player_index + 1) % self.num_players  # Fixed reference

        # Update the game screen to reflect the new state (current card and scores)
        self.update_card_indicator()  # Update cards left
        self.update_card()  # Update the displayed card
        self.update_player_labels_and_scores()  # Refresh player labels and scores

    def update_card(self):
        """Updates the displayed card image."""
        if self.is_second_card_visible:
            # Update the second card if it's visible
            self.card_image_2.source = self.current_card['image']
        self.update_card_indicator()

    def update_card_indicator(self):
        """Updates the card indicator label with the correct remaining card count."""
        cards_left = len([card for card in self.cards if not card['used']])
        
        # Prevent negative count (though this should rarely happen now)
        if cards_left < 0:
            cards_left = 0

        # Update the label text to reflect the cards left
        self.cards_left_label.text = f"Cards Left: {cards_left}"

    def display_scores(self):
        """Displays the final scores when the game ends."""
        score_text = "\n".join([f"Player {i+1}: {self.scores[i]} points" for i in range(self.num_players)])
        popup = Popup(title='Game Over', content=Label(text=score_text), size_hint=(0.5, 0.5))
        popup.open()

    def show_exit_popup(self, instance):
        """Show a confirmation popup when the user presses the exit button."""
        layout = FloatLayout()

        # Confirmation label
        label = Label(text="Are you sure you want to exit?", font_size=24, pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout.add_widget(label)

        # Yes button
        yes_button = Button(text="Yes", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.3, 'center_y': 0.4})
        yes_button.bind(on_press=lambda _: (self.reset_game(), setattr(self.manager, 'current', 'main_menu'), exit_popup.dismiss()))  # Reset the game on exit
        layout.add_widget(yes_button)

        # No button
        no_button = Button(text="No", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.7, 'center_y': 0.4})
        no_button.bind(on_press=lambda _: exit_popup.dismiss())
        layout.add_widget(no_button)

        # Create and open popup
        exit_popup = Popup(title='Confirm Exit', content=layout, size_hint=(0.8, 0.4))
        exit_popup.open()


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
