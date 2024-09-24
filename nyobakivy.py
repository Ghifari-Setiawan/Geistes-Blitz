from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
import random

Window.size = (1280, 720)

# Game variables
remaining_cards = 0
players = []
current_player_index = 0

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
        self.cards = []
        self.current_card = None

    def setup_game(self, num_players):
        self.items = self.create_items()
        self.cards = self.create_cards()
        global remaining_cards
        remaining_cards = len(self.cards)

        global players
        players = [{'name': f'Player {i+1}', 'score': 0} for i in range(num_players)]

        self.current_card = random.choice(self.cards)
        self.current_card['used'] = True

        self.update_game_screen()

    def create_items(self):
        return [
            {'name': 'Ghost', 'image': 'assets/setan.png'},
            {'name': 'Book', 'image': 'assets/buku.png'},
            {'name': 'Bottle', 'image': 'assets/botol.png'},
            {'name': 'Mouse', 'image': 'assets/tikus.png'},
            {'name': 'Sofa', 'image': 'assets/sofa.png'},
        ]

    def create_cards(self):
        return [
            {'image': 'assets/level1/card1.jpg', 'correct_item': 'Sofa', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level1/card2.jpg', 'correct_item': 'Ghost', 'incorrect_item': None, 'level': 1, 'used': False},
            {'image': 'assets/level2/card13.jpg', 'correct_item': None, 'incorrect_item': 'Mouse', 'level': 2, 'used': False},
            {'image': 'assets/level2/card14.jpg', 'correct_item': None, 'incorrect_item': 'Bottle', 'level': 2, 'used': False},
        ]

    def update_game_screen(self):
        self.clear_widgets()

        # Layout for the game screen
        layout = BoxLayout(orientation='vertical')

        # Display current card
        card_image = Image(source=self.current_card['image'], size_hint=(0.5, 0.5))
        layout.add_widget(card_image)

        # Display items
        item_layout = GridLayout(cols=5, size_hint=(1, 0.2))
        for item in self.items:
            item_button = Button(background_normal=item['image'])
            item_button.bind(on_release=lambda btn, item=item: self.handle_item_selection(item))
            item_layout.add_widget(item_button)

        layout.add_widget(item_layout)

        # Display remaining cards and scores
        info_layout = BoxLayout(size_hint=(1, 0.2))
        remaining_label = Label(text=f'Cards Left: {remaining_cards}', font_size='20sp')
        info_layout.add_widget(remaining_label)

        for player in players:
            player_label = Label(text=f"{player['name']}: {player['score']} pts", font_size='20sp')
            info_layout.add_widget(player_label)

        layout.add_widget(info_layout)

        self.add_widget(layout)

    def handle_item_selection(self, selected_item):
        global remaining_cards
        global current_player_index

        # Check current card level and validate selection
        if self.current_card['level'] == 1:
            if selected_item['name'] == self.current_card['correct_item']:
                players[current_player_index]['score'] += 1
                print(f"{players[current_player_index]['name']} selected the correct item!")
            else:
                print(f"{players[current_player_index]['name']} selected the wrong item!")
        elif self.current_card['level'] == 2:
            if selected_item['name'] != self.current_card['incorrect_item']:
                players[current_player_index]['score'] += 1
                print(f"{players[current_player_index]['name']} selected the correct item!")
            else:
                print(f"{players[current_player_index]['name']} selected the wrong item!")

        # Move to the next card or end the game
        next_card = next((card for card in self.cards if not card['used']), None)
        if next_card:
            self.current_card = next_card
            self.current_card['used'] = True
            remaining_cards -= 1
        else:
            print("No Cards Remaining!")
            self.display_scores()
            return

        current_player_index = (current_player_index + 1) % len(players)
        self.update_game_screen()

    def display_scores(self):
        score_text = "\n".join([f"{player['name']}: {player['score']} pts" for player in players])
        popup = Popup(title='Game Over', content=Label(text=score_text), size_hint=(0.5, 0.5))
        popup.open()

class PlayerSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        title = Label(text="Select Number of Players", font_size='40sp', size_hint=(1, 0.3))
        layout.add_widget(title)

        # Player selection buttons
        for i in range(2, 5):
            btn = Button(text=f"{i} Players", size_hint=(0.3, 0.1))
            btn.bind(on_release=lambda btn, i=i: self.start_game(i))
            layout.add_widget(btn)

        self.add_widget(layout)

    def start_game(self, num_players):
        self.manager.get_screen('game').setup_game(num_players)
        self.manager.current = 'game'


class HowToPlayPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        instructions = "\n".join([
            "1. Select the number of players.",
            "2. A card will be shown in the center.",
            "3. Players take turns selecting the correct item.",
            "4. Correct choices earn points, wrong choices do not.",
            "5. The game ends when all cards are used."
        ])
        self.content = Label(text=instructions)
        self.size_hint = (0.75, 0.75)
        self.title = 'How to Play'

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        title = Label(text="Geistes Blitz", font_size='40sp', size_hint=(1, 0.3))
        layout.add_widget(title)

        start_button = Button(text="Start", size_hint=(0.3, 0.1))
        start_button.bind(on_release=self.go_to_player_selection)
        layout.add_widget(start_button)

        instructions_button = Button(text="How To Play", size_hint=(0.3, 0.1))
        instructions_button.bind(on_release=self.show_instructions)
        layout.add_widget(instructions_button)

        self.add_widget(layout)

    def go_to_player_selection(self, instance):
        self.manager.current = 'player_selection'

    def show_instructions(self, instance):
        popup = HowToPlayPopup()
        popup.open()


class GeistesBlitzApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(PlayerSelectionScreen(name='player_selection'))
        sm.add_widget(GameScreen(name='game'))

        return sm


if __name__ == '__main__':
    GeistesBlitzApp().run()
