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
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
import random
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

# Set window size at the start
Window.size = (2340, 1080)

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
        )

        # Add How to Play button
        instructions_button = Button(
            size_hint=(0.3, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_normal='assets/howtoplay.png',  # Styled button image
        )

        start_button.bind(on_press=self.start_game)
        instructions_button.bind(on_press=self.show_instructions)

        layout.add_widget(start_button)
        layout.add_widget(instructions_button)

        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'player_selection'

    def show_instructions(self, instance):
        # Create a layout for the scrollable content
        content_layout = GridLayout(cols=1, spacing=15, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        # List of image sources and descriptions
        images_and_labels = [
            ('assets/howtoplay/welcome geistes blits.png', "1. Selamat Datang di Geistes Blitz\nTekan Start untuk memulai permainan!"),
            ('assets/howtoplay/select player geistes blits.png', "2. Pilih Jumlah Pemain\nPilih jumlah permain sesuai yang ingin dimainkan!"),
            ('assets/howtoplay/bagian permainan awal.png', "3. Bagian Permainan Awal\nTekan salah satu items untuk membuka kartu pertama!\nSetiap kali menekan items, kartu selanjutnya akan terbuka secara otomatis dan acak."),
            ('assets/howtoplay/pemilihan untuk kartu level 1.png', "4. Pemilihan Kartu Level 1\nKartu Level 1 berupa kartu yang berisi gambar dari items yang sesuai\ndengan bentuk dan warna dari items tersebut.\nJawablah dengan item dan warna yang sesuai dengan kartu tersebut!"),
            ('assets/howtoplay/pemilihan untuk kartu level 2.png', "5. Pemilihan Kartu Level 2\nKartu Level 2 berupa kartu yang berisi gambar dari items dengan bentuk dan warna\nyang tidak seharusnya dari items tersebut.\nJawablah dengan item dan warna yang tidak muncul pada kartu tersebut!"),
            ('assets/howtoplay/selesai permainan.png', "6. Permainan Selesai\nLihat hasil permainan pada popup yang muncul.\nTekan Restart Game untuk memulai kembali permainan!")
        ]

        # Add each image and its label to the layout
        for img_src, description in images_and_labels:
            label = Label(
                text=description,
                font_size='14sp',
                font_name='assets/fonts/CreteRound-Regular.ttf',
                size_hint_y=None,
                height=100,
                halign='center',
                valign='middle',
            )
            content_layout.add_widget(label)

            # Add image with defined size
            image = Image(source=img_src, size_hint_y=None, height=350)
            content_layout.add_widget(image)

        # Wrap the content layout in a scroll view
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(content_layout)

        # Create a main layout for the popup
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(scroll_view)

        # Add a close button at the bottom
        close_button = Button(text="Close", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.1})
        popup_layout.add_widget(close_button)

        # Create and show the popup
        popup = Popup(title='How to Play', content=popup_layout, size_hint=(0.8, 0.8))

        # Bind the close button to close the popup
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
        )
        
        three_players_button = Button(
            size_hint=(0.35, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_normal='assets/3players.png',
        )

        four_players_button = Button(
            size_hint=(0.35, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_normal='assets/4players.png',
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
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def start_game(self, num_players):
        """Starts the game with the specified number of players."""
        # Set the number of players
        self.num_player_count = num_players

        # Get the GameScreen and reset the game state
        game_screen = self.manager.get_screen('game_screen')
        game_screen.num_player_count = num_players

        # Reset and prepare the game layout for the new number of players
        game_screen.reset_game()

        # Add selection buttons based on the chosen number of players
        game_screen.add_selection_buttons()

        # Update player labels to match the player count if they exist
        if len(game_screen.player_labels) == num_players:
            game_screen.update_player_labels_and_scores()

        # Switch to the game screen
        self.manager.current = 'game_screen'
        
        # Debug message
        print(f"Game started with {num_players} players.")

    def go_back(self, instance):
        self.manager.current = 'main_menu'

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
        self.current_card_index += 0
        self.update_card_indicator()

        # Check if it's the last card, and trigger a win if needed
        if self.current_card_index >= len(self.cards):
            self.on_player_win(self.player_turn)


class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()  # Gunakan FloatLayout agar widget bisa bergerak
        self.add_widget(self.layout)

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameOverScreen(name='game_over_screen'))
        return sm

    def on_start(self):
        # Simulasi memanggil layar Game Over setelah aplikasi dimulai
        Clock.schedule_once(self.show_game_over, 2)

    def show_game_over(self, dt):
        # Pindah ke layar Game Over
        self.root.current = 'game_over_screen'


class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.num_players = [{'id': 0, 'name': 'Player 1'}, {'id': 1, 'name': 'Player 2'}, {'id': 2, 'name': 'Player 3'}, {'id': 3, 'name': 'Player 4'}]
        self.num_player_count = len(self.num_players)
        self.scores = [0] * self.num_player_count
        self.current_card_index = -1
        self.player_turn = 0
        self.is_second_card_visible = False
        self.current_player_index = 0
        self.cards = self.create_cards()
        self.create_game_layout()
        self.reset_game()
        self.card_image_2.source = 'assets/back_card.jpg'

    def reset_game(self):
        """Resets the game state, including cards and scores."""
        self.current_card_index = -1  # Start from the first card
        self.player_turn = 0
        self.scores = [0] * self.num_player_count  # Reset scores
        self.cards = self.create_cards()  # Reset card deck with fresh cards
        for card in self.cards:
            card['used'] = False  # Mark all cards as unused
        self.current_card = self.cards[self.current_card_index]  # Start with the first card
        self.current_card['used'] = True
        self.is_second_card_visible = False
        self.current_player_index = 0
        self.card_image_2.source = 'assets/back_card.jpg'

        # Reset player labels
        self.player_labels = []
        self.create_game_layout()  # Ensure the layout is rebuilt

        # Re-add player selection buttons based on player count
        self.add_selection_buttons()
        
        # Update labels if player_labels has been populated correctly
        if len(self.player_labels) == self.num_player_count:
            self.update_player_labels_and_scores()
        
        self.cards_left_label.text = f"Cards Left: {len(self.cards)}"  # Update initial count
        self.update_player_labels_and_scores()

    def create_game_layout(self):
        # Check if the layout already exists and clear it if necessary
        if hasattr(self, 'layout') and self.layout:
            self.layout.clear_widgets()  # Remove existing widgets to prevent duplication
        else:
            # Initialize the main layout if it doesn't exist
            self.layout = FloatLayout()

        self.layout = FloatLayout()
        self.items = self.create_items()
        self.cards = self.create_cards()
        self.current_card = self.cards[0]
        self.player_labels = []
        self.score_labels = []

        for i in range(self.num_player_count):
            player_label = Label(text=f"Player {i+1}", font_size=24, font_name='assets/fonts/CreteRound-Regular.ttf', pos_hint=self.get_player_position(i))
            score_label = Label(text=f"{self.scores[i]} pts", font_size=18, font_name='assets/fonts/RocknRollOne-Regular.ttf', pos_hint=self.get_player_score_position(i))
            self.player_labels.append(player_label)
            self.score_labels.append(score_label)
            self.layout.add_widget(player_label)
            self.layout.add_widget(score_label)

        self.update_player_labels_and_scores()
        self.back_card_button = self.add_back_card_button(pos_hint={'center_x': 0.4, 'center_y': 0.5})

        self.card_image_2 = self.add_card_at_position(None, pos_hint={'center_x': 0.6, 'center_y': 0.5})
        self.card_image_2.source = 'assets/back_card.jpg'

        self.cards_left_label = Label(text=f"Cards Left: {len(self.cards) - self.current_card_index}",
                                      font_size=24, font_name='assets/fonts/CreteRound-Regular.ttf', pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.layout.add_widget(self.cards_left_label)

        if self.current_card_index == -1 :
            self.start_label = Label(text="Press any item to start!",
                                    font_size=24, font_name='assets/fonts/CreteRound-Regular.ttf', pos_hint={'center_x': 0.5, 'center_y': 0.64})
            self.layout.add_widget(self.start_label)

        exit_button = ImageButton(source='assets/exit_icon_button.png', size_hint=(None, None), size=(64, 64),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.30})
        exit_button.bind(on_press=self.show_exit_popup)
        self.layout.add_widget(exit_button)

        self.clear_widgets()
        self.add_widget(self.layout)

    def add_back_card_button(self, pos_hint):
        """Adds a permanent back card button on the left for flipping to the next card."""
        back_card_button = ImageButton(source='assets/back_card.jpg', size_hint=(0.30, 0.30), pos_hint=pos_hint)
        self.layout.add_widget(back_card_button)
        return back_card_button

    def add_card_at_position(self, card, pos_hint):
        """Adds a card to the screen at a specified position."""
        # Initially set the card image to back_card.jpg
        card_image = ImageButton(source='assets/back_card.jpg', size_hint=(0.30, 0.30), pos_hint=pos_hint)
        self.layout.add_widget(card_image)
        return card_image

    def update_next_card(self):
        """Updates to the next unused card if available, and triggers card flip animation."""
        unused_cards = [card for card in self.cards if not card['used']]
        
        if unused_cards:
            # Select and mark the next card as used
            new_card = unused_cards[0]
            new_card['used'] = True
            self.current_card = new_card  # Update the current card to the new one
            self.current_card_index += 1  # Increment the card index

            # Trigger the card flip animation
            self.animate_card_flip(self.card_image_2, self.current_card, new_card)
            
            # Update the 'Cards Left' label
            self.cards_left_label.text = f"Cards Left: {len(unused_cards)}"
        else:
            print("No Cards Remaining!")
            self.display_scores()

    def animate_card_flip(self, card_image, current_card, new_card):
            
        if self.current_card_index == 0:
            # Set initial flip
            self.current_card_index = 0
            card_image.source = new_card['image']
        else:
            # Set new card image during subsequent flips
            card_image.source = new_card['image'] if new_card else current_card['image']

        # Animation logic remains the same
        flip_to_mid = Animation(size_hint_x=0, duration=0.2)
        flip_to_full = Animation(size_hint_x=0.30, duration=0.2)
        
        # After reaching the mid-flip, change the image to the card's front
        def reveal_front(*args):
            card_image.source = current_card['image'] if new_card is None else new_card['image']

        flip_to_mid.bind(on_complete=reveal_front)
        flip_to_mid.start(card_image)
        flip_to_mid.bind(on_complete=lambda *args: flip_to_full.start(card_image))

    def get_player_position(self, player_index):
        """Calculate player label positions."""
        positions = [{'center_x': 0.5, 'top': 0.90}, {'center_x': 0.1, 'center_y': 0.5}, 
                    {'center_x': 0.5, 'y': 0.49}, {'center_x': 0.9, 'center_y': 0.5}]
        return positions[player_index]

    def get_player_score_position(self, player_index):
        """Calculate score label positions."""
        positions = [{'center_x': 0.5, 'top': 0.55}, {'center_x': 0.1, 'center_y': 0.45}, 
                    {'center_x': 0.5, 'y': 0.43}, {'center_x': 0.9, 'center_y': 0.45}]
        return positions[player_index]
        
    def add_selection_buttons(self):
        """Adds selection buttons for each player based on the number of players."""

        # Define the positions based on the number of players
        positions = []
        if self.num_player_count == 2:
            positions = [
                {'center_x': 0.45, 'center_y': 0.17},  # Player 1 (bottom)
                {'center_x': 0.45, 'center_y': 0.80}   # Player 2 (top)
            ]
        elif self.num_player_count == 3:
            positions = [
                {'center_x': 0.45, 'center_y': 0.17},  # Player 1 (bottom)
                {'center_x': 0.25, 'center_y': 0.75},  # Player 2 (left)
                {'center_x': 0.95, 'center_y': 0.75}   # Player 3 (right)
            ]
        elif self.num_player_count == 4:
            positions = [
                {'center_x': 0.45, 'center_y': 0.17},  # Player 1 (bottom)
                {'center_x': 0.25, 'center_y': 0.75},   # Player 2 (left)
                {'center_x': 0.45, 'center_y': 0.80},  # Player 3 (top)
                {'center_x': 0.95, 'center_y': 0.75}   # Player 4 (right)
            ]
        else:
            print(f"Warning: Unsupported number of players ({self.num_player_count}).")
            return

        items = self.create_items()  # Get the list of items

        # Create buttons for each player
        for i in range(self.num_player_count):
            if self.num_player_count == 2:
                button_layout = GridLayout(cols=5, size_hint=(None, None), width=450, height=100, spacing=70)
                
            elif self.num_player_count == 3: 
                button_layout = GridLayout(cols=5 if i % 3 == 0 else 1, size_hint=(None, None), width=450, height=100, spacing=70)
                
            elif self.num_player_count == 4:
                button_layout = GridLayout(cols=5 if i % 2 == 0 else 1, size_hint=(None, None), width=450, height=100,spacing=70)
                
            for item in items:
                item_button = Button(
                    background_normal=item['image'],  # Ensure this path is correct
                    size_hint=(None, None),
                    size=(80, 80),
                    on_press=lambda btn, item=item, player_id=i: self.on_item_click(item, player_id)
                )
                button_layout.add_widget(item_button)


            button_layout.pos_hint = positions[i]  # Position for each player's layout
            self.layout.add_widget(button_layout)   # Add layout to the main layout



    def update_player_labels_and_scores(self):
        """Updates the player labels and scores."""
        # Ensure we only update labels for the number of existing players
        for i in range(self.num_player_count):  # Use self.num_player_count
            self.player_labels[i].text = f"Player {i+1}"
            self.player_labels[i].opacity = 1  # Make it visible
            self.score_labels[i].text = f"Score: {self.scores[i]}"
            self.score_labels[i].opacity = 1

        # Hide labels for non-existent players (if any)
        for i in range(self.num_player_count, len(self.player_labels)):  # Adjusted line
            self.player_labels[i].opacity = 0
            self.score_labels[i].opacity = 0

        self.update_player_positions()

    def update_player_positions(self):
        """Repositions players dynamically based on the number of players and screen layout."""

        if self.num_player_count == 2:
            print("Permainan sudah dimulai dengan 2 Players!")
            # Player 1 at the bottom, Player 2 at the top
            self.player_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.1}  # Centered near the bottom
            self.score_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.05}

            self.player_labels[1].pos_hint = {'center_x': 0.5, 'center_y': 0.95}  # Centered near the top
            self.score_labels[1].pos_hint = {'center_x': 0.5, 'center_y': 0.90}

        elif self.num_player_count == 3:
            print("Permainan sudah dimulai dengan 3 Players!")
            # Player 1 at the bottom, Player 2 on the left, Player 3 on the right
            self.player_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.1}  # Bottom center
            self.score_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.05}

            self.player_labels[1].pos_hint = {'center_x': 0.050, 'center_y': 0.5}  # Left center
            self.score_labels[1].pos_hint = {'center_x': 0.050, 'center_y': 0.45}

            self.player_labels[2].pos_hint = {'center_x': 0.95, 'center_y': 0.5}  # Right center
            self.score_labels[2].pos_hint = {'center_x': 0.95, 'center_y': 0.45}
            
        elif self.num_player_count == 4:
            print("Permainan sudah dimulai dengan 4 Players!")
            # Player 1 at the bottom, Player 2 on the left, Player 3 on the top, Player 4 on the right
            self.player_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.1}  # Bottom center
            self.score_labels[0].pos_hint = {'center_x': 0.5, 'center_y': 0.05}

            self.player_labels[1].pos_hint = {'center_x': 0.050, 'center_y': 0.5}  # Left center
            self.score_labels[1].pos_hint = {'center_x': 0.050, 'center_y': 0.45}

            self.player_labels[2].pos_hint = {'center_x': 0.5, 'center_y': 0.95}  # Top center
            self.score_labels[2].pos_hint = {'center_x': 0.5, 'center_y': 0.90}

            self.player_labels[3].pos_hint = {'center_x': 0.95, 'center_y': 0.5}  # Right center
            self.score_labels[3].pos_hint = {'center_x': 0.95, 'center_y': 0.45}

    def on_item_click(self, selected_item, player_id):
        self.handle_item_selection(selected_item, player_id)

    def create_items(self):
        """Defines the available items with images."""
        return [
            {'name': 'Ghost', 'image': 'assets/ghost2.jpg'},
            {'name': 'Book', 'image': 'assets/buku2.jpg'},
            {'name': 'Bottle', 'image': 'assets/botol2.jpg'},
            {'name': 'Mouse', 'image': 'assets/tikus2.jpg'},
            {'name': 'Sofa', 'image': 'assets/sofa2.jpg'},
        ]

    def create_cards(self):
        """Defines the cards, including correct and incorrect items."""
        cards = [
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
            {'image': 'assets/level2/card12.jpg', 'correct_item': None, 'incorrect_item': 'Sofa', 'level': 2, 'used': False},
            {'image': 'assets/level2/card13.jpg', 'correct_item': None, 'incorrect_item': 'Mouse', 'level': 2, 'used': False},
            {'image': 'assets/level2/card14.jpg', 'correct_item': None, 'incorrect_item': 'Bottle', 'level': 2, 'used': False},
            {'image': 'assets/level2/card15.jpg', 'correct_item': None, 'incorrect_item': 'Mouse', 'level': 2, 'used': False},
            {'image': 'assets/level2/card16.jpg', 'correct_item': None, 'incorrect_item': 'Book', 'level': 2, 'used': False},
            {'image': 'assets/level2/card17.jpg', 'correct_item': None, 'incorrect_item': 'Book', 'level': 2, 'used': False},
            {'image': 'assets/level2/card18.jpg', 'correct_item': None, 'incorrect_item': 'Bottle', 'level': 2, 'used': False},
            {'image': 'assets/level2/card19.jpg', 'correct_item': None, 'incorrect_item': 'Mouse', 'level': 2, 'used': False},
            {'image': 'assets/level2/card20.jpg', 'correct_item': None, 'incorrect_item': 'Bottle', 'level': 2, 'used': False},
        ]

        # Shuffle the cards to ensure random order
        random.shuffle(cards)
        return cards
    
    def show_feedback_popup(self, message, player_id):
        """Displays a pop-up with feedback message."""
        content = Label(text=message, font_size=20)
        popup = Popup(
            title=f"Player {player_id + 1}", 
            content=content,
            size_hint=(None, None), 
            size=(300, 200),
            auto_dismiss=False
        )
        popup.open()

        # Schedule the pop-up to dismiss after 2 seconds
        Clock.schedule_once(lambda dt: popup.dismiss(), 1)

    def handle_item_selection(self, selected_item, player_id):
        if hasattr(self, 'start_label') and self.start_label in self.layout.children:
            self.layout.remove_widget(self.start_label)

        # Start the game with the first card if it's the first item selection
        if self.current_card_index == -1:
            self.update_next_card()
            print("Game started!")
            return

        # Determine feedback message based on correctness
        if self.current_card['level'] == 1:
            if selected_item['name'] == self.current_card['correct_item']:
                self.scores[player_id] += 1
                message = f"Correct! Player {player_id + 1} scores."
                # Move to the next card if the answer is correct
                self.update_next_card()
            else:
                message = f"Wrong! Player {player_id + 1} missed it."
                # Stay on the current card
        elif self.current_card['level'] == 2:
            if selected_item['name'] == self.current_card['incorrect_item']:
                self.scores[player_id] += 1
                message = f"Correct! Player {player_id + 1} scores."
                # Move to the next card if the answer is correct
                self.update_next_card()
            else:
                message = f"Wrong! Player {player_id + 1} missed it."
                # Stay on the current card

        # Show feedback popup with the message
        self.show_feedback_popup(message, player_id)

        # Update player labels and scores after selection
        self.update_player_labels_and_scores()

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
        self.cards_left_label.text = f"Cards Left: {len(self.cards)}"

    def display_scores(self):
        """Displays the final scores when the game ends with options to restart or return to the main menu."""
        
        # Create score text
        score_text = "\n".join([f"Player {i+1}: {self.scores[i]} points" for i in range(self.num_player_count)])
        score_label = Label(text=score_text)

        # Create buttons for "Restart Game" and "Main Menu"
        restart_button = Button(text="Restart Game", size_hint=(1, 0.2))
        main_menu_button = Button(text="Main Menu", size_hint=(1, 0.2))
        
        # Define the actions for the buttons
        restart_button.bind(on_press=lambda _: (self.reset_game(), popup.dismiss()))
        main_menu_button.bind(on_press=lambda _: (self.reset_game(), setattr(self.manager, 'current', 'main_menu'), popup.dismiss()))

        # Create a layout for the buttons and score label
        box_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box_layout.add_widget(score_label)
        box_layout.add_widget(restart_button)
        box_layout.add_widget(main_menu_button)

        # Create and open the popup
        popup = Popup(title='Game Over', content=box_layout, size_hint=(0.6, 0.6), auto_dismiss=False)
        popup.open()

    def show_exit_popup(self, instance):
        """Show a confirmation popup when the user presses the exit button."""
        layout = FloatLayout()

        # Confirmation label
        label = Label(text="Quit Game", font_size=28, pos_hint={'center_x': 0.5, 'center_y': 0.75})
        layout.add_widget(label)

        # Yes button
        yes_button = Button(text="Yes", size_hint=(0.25, 0.25), pos_hint={'center_x': 0.3, 'center_y': 0.3})
        yes_button.bind(on_press=lambda _: (self.reset_game(), setattr(self.manager, 'current', 'main_menu'), exit_popup.dismiss()))  # Reset the game on exit
        layout.add_widget(yes_button)

        # No button
        no_button = Button(text="No", size_hint=(0.25, 0.25), pos_hint={'center_x': 0.7, 'center_y': 0.3})
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
