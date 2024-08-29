import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set screen dimensions
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Geistes Blitz')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load fonts
font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 36)

# Button Class
class Button:

    pygame.init()

    def __init__(self, text, pos, size):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = GRAY
        self.rect = pygame.Rect(self.pos, self.size)
        self.text_surf = button_font.render(self.text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered(pygame.mouse.get_pos()):
                return True
        return False

def start_screen():

    pygame.init()

    start_button = Button('Start', (560, 250), (110, 50))
    instructions_button = Button('How To Play', (520, 350), (200, 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.handle_event(event):
                player_selection_screen()
            if instructions_button.handle_event(event):
                instructions_screen()

        screen.fill(WHITE)
        start_button.draw(screen)
        instructions_button.draw(screen)
        pygame.display.flip()

def player_selection_screen():

    pygame.init()

    two_players_button = Button('2 Players', (520, 200), (200, 50))
    three_players_button = Button('3 Players', (520, 300), (200, 50))
    four_players_button = Button('4 Players', (520, 400), (200, 50))

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if two_players_button.handle_event(event):
                game_loop(2)
            if three_players_button.handle_event(event):
                game_loop(3)
            if four_players_button.handle_event(event):
                game_loop(4)

        screen.fill(WHITE)
        two_players_button.draw(screen)
        three_players_button.draw(screen)
        four_players_button.draw(screen)
        pygame.display.flip()

def instructions_popup():
    # Instructions text
    instructions = [
        "How to Play:",
        "1. Select the number of players.",
        "2. A card will be shown in the center.",
        "3. Players take turns selecting the correct item.",
        "4. Correct choices earn points, wrong choices do not.",
        "5. The game ends when all cards are used."
    ]

    # Set popup size and position
    popup_width, popup_height = 750, 350
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    # Draw popup background
    pygame.draw.rect(screen, GRAY, popup_rect)

    # Draw instructions text
    for i, line in enumerate(instructions):
        instructions_text = button_font.render(line, True, BLACK)
        screen.blit(instructions_text, (popup_x + 20, popup_y + 20 + i * 30))

    # Draw close button
    close_button = Button('Close', (popup_x + popup_width // 2 - 50, popup_y + popup_height - 60), (100, 40))
    close_button.draw(screen)

    pygame.display.flip()

    # Event loop for popup
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if close_button.handle_event(event):
                return  # Exit the popup

def instructions_screen():

    pygame.init()

    # Immediately open the popup
    screen.fill(WHITE)
    pygame.display.flip()
    instructions_popup()  # Call the popup function
    start_screen()  # Return to the start screen after closing the popup

def draw_game_screen(current_card, items, players):
    screen.fill(WHITE)

    # Draw the current card in the center
    screen.blit(current_card.image, (screen_width // 2 - current_card.rect.width // 2, screen_height // 2 - current_card.rect.height // 2))

    # Position settings based on the number of players
    player_positions = [
    {'score_pos': (screen_width // 2, screen_height - 50), 'item_pos': (screen_width // 2 - 150, screen_height - 150), 'rotation': 0},  # Bottom (Player 1)
    {'score_pos': (screen_width // 2, 50), 'item_pos': (screen_width // 2 - 150, 100), 'rotation': 180},  # Top (Player 2)
    {'score_pos': (50, screen_height // 2), 'item_pos': (100, screen_height // 2 - 100), 'rotation': 270},  # Left (Player 3) 
    {'score_pos': (screen_width - 50, screen_height // 2), 'item_pos': (screen_width - 150, screen_height // 2 - 100), 'rotation': -270},  # Right (Player 4)
    ]

    # Scaling down items if necessary
    scaled_items = []
    for item in items:
        scaled_item_image = pygame.transform.scale(item.image, (80, 80))  # Scale to fit better
        scaled_items.append(scaled_item_image)

    # Draw player items and scores
    for i, player in enumerate(players):
        pos = player_positions[i]
        # Draw score
        score_text = font.render(f"{player['name']}: {player['score']} poin", True, BLACK)
        rotated_score_text = pygame.transform.rotate(score_text, pos['rotation'])
        screen.blit(rotated_score_text, rotated_score_text.get_rect(center=pos['score_pos']))

        # Draw items
        for j, item_image in enumerate(scaled_items):
            item_rect = item_image.get_rect(topleft=(pos['item_pos'][0] + j * 100, pos['item_pos'][1]))
            rotated_item_image = pygame.transform.rotate(item_image, pos['rotation'])
            screen.blit(rotated_item_image, item_rect)

    pygame.display.flip()


class Item(pygame.sprite.Sprite):
    def __init__(self, name, color, image_path, pos):
        super().__init__()
        self.name = name
        self.color = color
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

def create_items():
    item_positions = [(100, 400), (250, 400), (400, 400), (550, 400), (700, 400)]
    items = [
        Item('Ghost', WHITE, 'assets/setan.png', item_positions[0]),
        Item('Book', BLUE, 'assets/buku.png', item_positions[1]),
        Item('Bottle', GREEN, 'assets/botol.png', item_positions[2]),
        Item('Mouse', GRAY, 'assets/tikus.png', item_positions[3]),
        Item('Sofa', RED, 'assets/sofa.png', item_positions[4]),
    ]
    return items

class Card(pygame.sprite.Sprite):
    def __init__(self, image_path, correct_item, incorrect_item, level):
        super().__init__()
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (200, 300))  # Ubah ukuran gambar kartu
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 3))
        self.correct_item = correct_item
        self.incorrect_item = incorrect_item
        self.level = level
        self.used = False  # Track if the card has been used

def create_cards():
    cards = [
        Card('assets/level1/card1.jpg', 'Sofa', None, 1),
        Card('assets/level1/card2.jpg', 'Ghost', None, 1),
        Card('assets/level2/card13.jpg', None, 'Sofa', 2),
        Card('assets/level2/card14.jpg', None, 'Sofa', 2),
    ]
    return cards

def display_scores(players):
    # Placeholder function to display final scores
    print("Final Scores:")
    for player in players:
        print(f"{player['name']}: {player['score']} poin")

def handle_item_selection(selected_item, current_card, players, current_player_index, cards):
    # Check current card level and validate selection
    if current_card.level == 1:
        if selected_item.name == current_card.correct_item:
            players[current_player_index]['score'] += 1
            print(f"{players[current_player_index]['name']} selected the correct item!")
        else:
            print(f"{players[current_player_index]['name']} selected the wrong item!")
    elif current_card.level == 2:
        if selected_item.name != current_card.incorrect_item:
            players[current_player_index]['score'] += 1
            print(f"{players[current_player_index]['name']} selected the correct item!")
        else:
            print(f"{players[current_player_index]['name']} selected the wrong item!")

    # Move to the next round or end the game if cards are finished
    next_card = next((card for card in cards if not card.used), None)
    if next_card:
        current_card = next_card
        current_card.used = True
    else:
        print("No Cards Remaining!")
        display_scores(players)
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # Return the updated current card
    return current_card

def game_loop(num_players):

    pygame.init()

    # Initialize items and cards
    items = create_items()
    cards = create_cards()

    # Initialize player data based on the number of players
    players = [{'name': f'Player {i+1}', 'score': 0} for i in range(num_players)]

    current_card = random.choice(cards)  # Get the first card
    current_card.used = True  # Mark card as used
    current_player_index = 0  # Start with the first player

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle item selection
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in items:
                    if item.rect.collidepoint(event.pos):
                        current_card = handle_item_selection(item, current_card, players, current_player_index, cards)
                        current_player_index = (current_player_index + 1) % num_players  # Move to the next player

        draw_game_screen(current_card, items, players)  # Send players list to the draw function

    pygame.quit()

# Main loop
start_screen()