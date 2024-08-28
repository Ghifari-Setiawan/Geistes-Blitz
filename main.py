import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Geistes Blitz')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
DARK_GREY = (100, 100, 100)

# Load fonts
font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 36)

# Button class
class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = GREY
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


def title_screen():
    start_button = Button('Start', (300, 150), (200, 50))
    how_to_play_button = Button('How To Play', (300, 250), (200, 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.handle_event(event):
                select_player_screen()
            if how_to_play_button.handle_event(event):
                how_to_play_screen()

        screen.fill(WHITE)
        start_button.draw(screen)
        how_to_play_button.draw(screen)
        pygame.display.flip()


def game_screen(num_players):
    
    pygame.init()

    # Screen dimensions
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Geistes Blitz")

    # Colors
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    BLACK = (0, 0, 0)

    # Font
    font = pygame.font.SysFont(None, 40)

    # Player data (using num_players to initialize the correct number of players)
    players = [{'name': f'Player {i+1}', 'score': 0} for i in range(num_players)]

    def draw_game_screen(current_card, items):
        screen.fill(WHITE)

        # Draw the current card in the center
        screen.blit(current_card.image, (screen_width // 2 - current_card.rect.width // 2, screen_height // 3))

        # Draw item options for selection
        for item in items:
            screen.blit(item.image, item.rect.topleft)

        # Draw player scores (only for the number of active players)
        for i, player in enumerate(players):
            player_score_text = font.render(f"{player['name']}: {player['score']} pts", True, BLACK)
            screen.blit(player_score_text, (20, 20 + i * 40))

        pygame.display.flip()

    def game_loop():
        # Initialize items and cards
        items = create_items()
        cards = create_cards()

        current_card = random.choice(cards)  # Draw the first card

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle item selection
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in items:
                        if item.rect.collidepoint(event.pos):
                            handle_item_selection(item, current_card)

            draw_game_screen(current_card, items)

        pygame.quit()

    # Call the game loop to start the game
    game_loop()


def select_player_screen():
    player2_button = Button('2 Player', (300, 150), (200, 50))
    player3_button = Button('3 Player', (300, 250), (200, 50))
    player4_button = Button('4 Player', (300, 350), (200, 50))

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if player2_button.handle_event(event):
                game_screen(2)
            if player3_button.handle_event(event):
                game_screen(3)
            if player4_button.handle_event(event):
                game_screen(4)

        screen.fill(WHITE)
        player2_button.draw(screen)
        player3_button.draw(screen)
        player4_button.draw(screen)
        pygame.display.flip()


def how_to_play_screen():
    skip_button = Button('Skip', (screen_width - 120, screen_height - 70), (100, 50))
    
    # Load or render video here if needed (omitted for simplicity)
    
    watching = True
    while watching:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if skip_button.handle_event(event):
                watching = False
                title_screen()

        screen.fill(WHITE)
        # Display instructions or video here
        skip_button.draw(screen)
        pygame.display.flip()

class Item(pygame.sprite.Sprite):
    def __init__(self, name, color, image_path, pos):
        super().__init__()
        self.name = name
        self.color = color
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

# Color definitions
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

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

def handle_item_selection(selected_item, current_card):
    # Example of selection logic based on card level
    if current_card.level == 1:
        if selected_item.name == current_card.correct_item:
            print("Correct!")
            # Update score and proceed to the next card
        else:
            print("Incorrect!")
    elif current_card.level == 2:
        if selected_item.name != current_card.incorrect_item:
            print("Correct!")
            # Update score and proceed to the next card
        else:
            print("Incorrect!")


class Card(pygame.sprite.Sprite):
    def __init__(self, image_path, correct_item, incorrect_item, level):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 3))
        self.correct_item = correct_item
        self.incorrect_item = incorrect_item
        self.level = level

def create_cards():
    cards = [
        Card('card1.png', 'Ghost', None, 1),
        Card('card2.png', 'Book', None, 1),
        Card('card3.png', None, 'Bottle', 2),
        Card('card4.png', None, 'Mouse', 2),
        # Add more cards as needed
    ]
    return cards


# Create buttons
start_button = Button('Start', (300, 150), (200, 50))
how_to_play_button = Button('How To Play', (300, 250), (200, 50))

# Game loop flag
running = True

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle button clicks
        if start_button.handle_event(event):
            print("Start Game Clicked")
            select_player_screen()

        if how_to_play_button.handle_event(event):
            print("How To Play Clicked")
            how_to_play_screen()

    # Clear screen
    screen.fill(WHITE)

    # Draw UI elements
    start_button.draw(screen)
    how_to_play_button.draw(screen)

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
