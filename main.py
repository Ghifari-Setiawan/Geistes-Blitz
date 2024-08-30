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
    def __init__(self, text, pos, size, base_color, hover_color):
        self.text = text
        self.pos = pos
        self.size = size
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.rect = pygame.Rect(self.pos, self.size)
        self.text_surf = button_font.render(self.text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, RED, self.rect, 2)  # Add a red border
        screen.blit(self.text_surf, self.text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.is_hovered(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.base_color

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered(pygame.mouse.get_pos()):
                return True
        return False


def start_screen():

    start_button = Button('Start', (560, 250), (160, 60), GRAY, DARK_GRAY)
    instructions_button = Button('How To Play', (520, 350), (240, 60), GRAY, DARK_GRAY)

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

        screen.fill((0, 64, 128))  # Background color matching the image
        start_button.draw(screen)
        instructions_button.draw(screen)
        pygame.display.flip()


def player_selection_screen():
    two_players_button = Button('2 Players', (540, 200), (200, 60), GRAY, DARK_GRAY)
    three_players_button = Button('3 Players', (540, 300), (200, 60), GRAY, DARK_GRAY)
    four_players_button = Button('4 Players', (540, 400), (200, 60), GRAY, DARK_GRAY)

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

        screen.fill((0, 64, 128))  # Background color matching the image
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
    pygame.init()
    screen.fill(WHITE)

    # Draw the current card in the center
    screen.blit(current_card.image, (screen_width // 2 - current_card.rect.width // 2, screen_height // 2 - current_card.rect.height // 2))

    # Position settings for players
    player_positions = [
        {'score_pos': (screen_width // 2, screen_height - 30), 'item_pos': [(screen_width // 2 - 200 + i * 80, screen_height // 2 + 180) for i in range(5)]},  # Bottom (Player 1)
        {'score_pos': (screen_width // 2, 30), 'item_pos': [(screen_width // 2 - 200 + i * 100, 100) for i in range(5)]},  # Top (Player 2)
        {'score_pos': (30, screen_height // 2 + 170), 'item_pos': [(100, screen_height // 2 - 200 + i * 80) for i in range(5)], 'vertical': True, 'facing_right': True},  # Left (Player 3)
        {'score_pos': (screen_width - 30, screen_height // 2 + 170), 'item_pos': [(screen_width - 150, screen_height // 2 - 200 + i * 100) for i in range(5)], 'vertical': True, 'facing_left': True},  # Right (Player 4)
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
        score_text = font.render(f"{player['name']}: {player['score']} pts", True, BLACK)

        if 'vertical' in pos:
            score_text = pygame.transform.rotate(score_text, 90)
            if 'facing_right' in pos:
                score_text = pygame.transform.rotate(score_text, 180)
            elif 'facing_left' in pos: 
                score_text = pygame.transform.rotate(score_text, 0)
            screen.blit(score_text, score_text.get_rect(center=(pos['score_pos'][0], pos['score_pos'][1] - 150)))
        else:
            screen.blit(score_text, score_text.get_rect(center=pos['score_pos']))

        # Draw items
        for j, item_image in enumerate(scaled_items):
            item_rect = item_image.get_rect(topleft=pos['item_pos'][j])

            # Rotate items for Player 3 and 4
            if 'facing_right' in pos:
                item_image = pygame.transform.rotate(item_image, -90)
            elif 'facing_left' in pos:
                item_image = pygame.transform.rotate(item_image, 90)

            screen.blit(item_image, item_rect)

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
        Card('assets/level2/card13.jpg', None, 'Mouse', 2),
        Card('assets/level2/card14.jpg', None, 'Bottle', 2),
    ]
    return cards

def display_scores(players):
    # Placeholder function to display final scores
    print("Final Scores:")
    for player in players:
        print(f"{player['name']}: {player['score']} pts")

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
