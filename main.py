import pygame
import sys
import random

# Inisialisasi pygame
pygame.init()

# Tetapkan dimensi layar
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Geistes Blitz')

# Definisikan warna
PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)
ABU_ABU = (192, 192, 192)
ABU_ABU_TUA = (100, 100, 100)

# Muat font
font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 36)

# Kelas Tombol
class Tombol:
    def __init__(self, teks, pos, ukuran):
        self.teks = teks
        self.pos = pos
        self.ukuran = ukuran
        self.warna = ABU_ABU
        self.rect = pygame.Rect(self.pos, self.ukuran)
        self.text_surf = button_font.render(self.teks, True, HITAM)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.warna, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered(pygame.mouse.get_pos()):
                return True
        return False

def layar_awal():
    tombol_mulai = Tombol('Mulai', (300, 150), (200, 50))
    tombol_cara_bermain = Tombol('Cara Bermain', (300, 250), (200, 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if tombol_mulai.handle_event(event):
                layar_pilih_pemain()
            if tombol_cara_bermain.handle_event(event):
                layar_cara_bermain()

        screen.fill(PUTIH)
        tombol_mulai.draw(screen)
        tombol_cara_bermain.draw(screen)
        pygame.display.flip()

def layar_pilih_pemain():
    tombol_pemain2 = Tombol('2 Pemain', (300, 150), (200, 50))
    tombol_pemain3 = Tombol('3 Pemain', (300, 250), (200, 50))
    tombol_pemain4 = Tombol('4 Pemain', (300, 350), (200, 50))

    memilih = True
    while memilih:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if tombol_pemain2.handle_event(event):
                game_loop(2)
            if tombol_pemain3.handle_event(event):
                game_loop(3)
            if tombol_pemain4.handle_event(event):
                game_loop(4)

        screen.fill(PUTIH)
        tombol_pemain2.draw(screen)
        tombol_pemain3.draw(screen)
        tombol_pemain4.draw(screen)
        pygame.display.flip()

def popup_cara_bermain():
    # Teks instruksi
    instruksi = [
        "Cara Bermain:",
        "1. Pilih jumlah pemain.",
        "2. Kartu akan ditampilkan di tengah.",
        "3. Pemain bergiliran memilih item yang benar.",
        "4. Pilihan yang benar mendapatkan poin, yang salah tidak.",
        "5. Permainan berakhir saat semua kartu digunakan."
    ]
    
    # Latar belakang popup
    popup_rect = pygame.Rect(100, 100, 600, 400)
    pygame.draw.rect(screen, ABU_ABU, popup_rect)
    
    # Gambar teks instruksi
    for i, line in enumerate(instruksi):
        teks_instruksi = button_font.render(line, True, HITAM)
        screen.blit(teks_instruksi, (popup_rect.x + 20, popup_rect.y + 20 + i * 40))
    
    # Gambar tombol tutup
    tombol_tutup = Tombol('Tutup', (350, 450), (100, 50))
    tombol_tutup.draw(screen)
    
    pygame.display.flip()
    
    # Loop event untuk popup
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if tombol_tutup.handle_event(event):
                return  # Keluar dari popup

def layar_cara_bermain():
    # Langsung membuka popup
    screen.fill(PUTIH)
    pygame.display.flip()
    popup_cara_bermain()  # Panggil fungsi popup
    layar_awal()  # Kembali ke layar awal setelah menutup popup

def draw_game_screen(current_card, items, players):
    screen.fill(PUTIH)

    # Gambar kartu saat ini di tengah
    screen.blit(current_card.image, (screen_width // 2 - current_card.rect.width // 2, screen_height // 3))

    # Gambar opsi item untuk dipilih
    for item in items:
        screen.blit(item.image, item.rect.topleft)

    # Gambar skor pemain (hanya untuk jumlah pemain aktif)
    for i, player in enumerate(players):
        teks_skor_pemain = font.render(f"{player['name']}: {player['score']} pts", True, HITAM)
        screen.blit(teks_skor_pemain, (20, 20 + i * 40))

    pygame.display.flip()

class Item(pygame.sprite.Sprite):
    def __init__(self, name, color, image_path, pos):
        super().__init__()
        self.name = name
        self.color = color
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

# Definisi warna
PUTIH = (255, 255, 255)
BIRU = (0, 0, 255)
HIJAU = (0, 255, 0)
ABU_ABU = (128, 128, 128)
MERAH = (255, 0, 0)

def buat_item():
    posisi_item = [(100, 400), (250, 400), (400, 400), (550, 400), (700, 400)]
    items = [
        Item('Hantu', PUTIH, 'assets/setan.png', posisi_item[0]),
        Item('Buku', BIRU, 'assets/buku.png', posisi_item[1]),
        Item('Botol', HIJAU, 'assets/botol.png', posisi_item[2]),
        Item('Tikus', ABU_ABU, 'assets/tikus.png', posisi_item[3]),
        Item('Sofa', MERAH, 'assets/sofa.png', posisi_item[4]),
    ]
    return items

class Kartu(pygame.sprite.Sprite):
    def __init__(self, image_path, correct_item, incorrect_item, level):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 3))
        self.correct_item = correct_item
        self.incorrect_item = incorrect_item
        self.level = level
        self.used = False  # Melacak apakah kartu sudah digunakan

def buat_kartu():
    kartu = [
        Kartu('assets/level1/card1.jpg', 'Hantu', None, 1),
        Kartu('assets/level1/card2.jpg', 'Buku', None, 1),
        Kartu('assets/level2/card13.jpg', None, 'Botol', 2),
        Kartu('assets/level2/card14.jpg', None, 'Tikus', 2),
    ]
    return kartu

def tampilkan_skor(players):
    # Fungsi placeholder untuk menampilkan skor akhir
    print("Skor Akhir:")
    for player in players:
        print(f"{player['name']}: {player['score']} pts")

def handle_item_selection(selected_item, current_card, players, current_player_index, cards):
    # Periksa level kartu saat ini dan validasi pilihan
    if current_card.level == 1:
        if selected_item.name == current_card.correct_item:
            players[current_player_index]['score'] += 1
            print(f"{players[current_player_index]['name']} memilih item yang benar!")
        else:
            print(f"{players[current_player_index]['name']} memilih item yang salah!")
    elif current_card.level == 2:
        if selected_item.name != current_card.incorrect_item:
            players[current_player_index]['score'] += 1
            print(f"{players[current_player_index]['name']} memilih item yang benar!")
        else:
            print(f"{players[current_player_index]['name']} memilih item yang salah!")

    # Lanjutkan ke ronde berikutnya atau akhiri permainan jika kartu habis
    next_card = next((card for card in cards if not card.used), None)
    if next_card:
        current_card = next_card
        current_card.used = True
    else:
        print("Permainan Selesai!")
        tampilkan_skor(players)
        pygame.quit()
        sys.exit()

    # Kembalikan kartu saat ini yang diperbarui
    return current_card

def game_loop(num_players):
    # Inisialisasi item dan kartu
    items = buat_item()
    cards = buat_kartu()

    # Inisialisasi data pemain berdasarkan jumlah pemain
    players = [{'name': f'Pemain {i+1}', 'score': 0} for i in range(num_players)]

    current_card = random.choice(cards)  # Ambil kartu pertama
    current_card.used = True  # Tandai kartu sebagai digunakan
    current_player_index = 0  # Mulai dengan pemain pertama

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Menangani pemilihan item
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in items:
                    if item.rect.collidepoint(event.pos):
                        current_card = handle_item_selection(item, current_card, players, current_player_index, cards)
                        current_player_index = (current_player_index + 1) % num_players  # Pindah ke pemain berikutnya

        draw_game_screen(current_card, items, players)  # Kirim daftar pemain ke fungsi draw

    pygame.quit()

# Loop utama
layar_awal()
