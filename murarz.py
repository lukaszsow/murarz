import pygame
import random
import sys
import os

pygame.init()

# Ustawienia
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulator Murarza")

font = pygame.font.SysFont(None, 36)

# Kolory
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (30, 30, 30)
GREEN = (0, 200, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 215, 0)
RED = (200, 0, 0)
BUTTON_BG = (40, 40, 40)

# Dane gracza
exp = 0
money = 0
level = 1
exp_to_next = 100
current_mortar = "Podstawowa zaprawa"
owned_mortars = ["Podstawowa zaprawa"]
last_unboxed_mortar = None

# Ulepszenia
upgrades = {
    "szpachelka": 1,
    "ubranie": 1,
    "stawianie": 1
}

# Lista zapraw
mortars = [
    ("Zaprawa z piwem", "common"),
    ("Zaprawa turbo", "common"),
    ("Zaprawa premium", "uncommon"),
    ("Zaprawa złota", "rare"),
    ("Zaprawa diamentowa", "epic"),
    ("Zaprawa mistyczna", "legendary"),
    ("Zaprawa bogów", "mythical"),
    ("Zaprawa chaosu", "mythical"),
    ("Zaprawa czasoprzestrzenna", "mythical"),
    ("Zaprawa ostateczna", "mythical"),
]

# Skrzynki
boxes = {
    "Drewniana Skrzynka": {"price": 50, "chances": {"common": 70, "uncommon": 25, "rare": 5}},
    "Złota Skrzynka": {"price": 150, "chances": {"common": 30, "uncommon": 40, "rare": 25, "epic": 5}},
    "Boska Skrzynka": {"price": 500, "chances": {"rare": 20, "epic": 40, "legendary": 30, "mythical": 10}},
}

# Przyciski
brick_button = pygame.Rect(100, 500, 200, 50)
box_button = pygame.Rect(500, 500, 200, 50)
select_mortar_button = pygame.Rect(320, 500, 150, 50)
back_button = pygame.Rect(650, 50, 120, 40)

brick_img = pygame.image.load("brick.png")
box_img = pygame.image.load("box.png")
mortar_img = pygame.image.load("mortar.png")


# Dopasuj rozmiary obrazków do przycisków
brick_img = pygame.transform.scale(brick_img, (brick_button.width, brick_button.height))
box_img = pygame.transform.scale(box_img, (box_button.width, box_button.height))
mortar_img = pygame.transform.scale(mortar_img, (select_mortar_button.width, select_mortar_button.height))


# Stan gry
mode = "main"
building_wall_timer = 0
level_up_message_timer = 0
building_animation_frames = []
building_frame_index = 0
building_animation_duration = 1000  # ms

# Wczytaj animację gif (ramki)
for i in range(10):
    path = f"images/building_animation/frame_{i}.png"
    if os.path.exists(path):
        frame = pygame.image.load(path).convert()
        building_animation_frames.append(pygame.transform.scale(frame, (WIDTH, HEIGHT)))

# Funkcje
def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def place_brick():
    global exp, money, mode, building_wall_timer, building_frame_index
    rarity_bonus = {
        "common": (15, 20, (5, 8)),
        "uncommon": (20, 25, (8, 12)),
        "rare": (25, 30, (12, 18)),
        "epic": (30, 35, (18, 25)),
        "legendary": (35, 40, (25, 35)),
        "mythical": (40, 50, (35, 50))
    }
    current_rarity = get_mortar_rarity(current_mortar)
    exp_gain_range, money_gain_range = rarity_bonus[current_rarity][:2], rarity_bonus[current_rarity][2]

    exp_gain = random.randint(*exp_gain_range)
    money_gain = random.randint(*money_gain_range)

    exp += exp_gain * upgrades["szpachelka"]
    money += money_gain * upgrades["szpachelka"]

    level_up_check()
    building_wall_timer = pygame.time.get_ticks()
    building_frame_index = 0
    mode = "building_wall"

def open_box(selected_box):
    global money, last_unboxed_mortar, mode
    if selected_box not in boxes:
        return
    box = boxes[selected_box]
    real_price = int(box["price"] * (1 - 0.1 * (upgrades["ubranie"] - 1)))
    if money >= real_price:
        money -= real_price
        roll = random.randint(1, 100)
        cumulative = 0
        for rarity, chance in box["chances"].items():
            cumulative += chance
            if roll <= cumulative:
                new_mortars = [m for m in mortars if m[1] == rarity]
                if new_mortars:
                    mortar = random.choice(new_mortars)[0]
                    last_unboxed_mortar = mortar
                    if mortar not in owned_mortars:
                        owned_mortars.append(mortar)
                    mode = "showing_unbox"
                break

def get_mortar_rarity(name):
    for mortar, rarity in mortars:
        if mortar == name:
            return rarity
    return "common"

def choose_mortar(index):
    global current_mortar
    if 0 <= index < len(owned_mortars):
        current_mortar = owned_mortars[index]

def level_up_check():
    global exp, level, exp_to_next, mode, level_up_message_timer
    while exp >= exp_to_next:
        exp -= exp_to_next
        level += 1
        exp_to_next = int(exp_to_next * 1.2)
        level_up_message_timer = pygame.time.get_ticks()
        mode = "upgrade_choice" if level % 5 == 0 else "level_up"

def apply_upgrade(choice):
    global mode
    if choice in upgrades:
        upgrades[choice] += 1
    mode = "main"

# Główna pętla gry
clock = pygame.time.Clock()
while True:
    screen.fill(DARK_GRAY)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == "main":
                if brick_button.collidepoint(event.pos):
                    place_brick()
                elif box_button.collidepoint(event.pos):
                    mode = "choosing_box"
                elif select_mortar_button.collidepoint(event.pos):
                    mode = "choosing_mortar"
            elif mode == "choosing_box":
                if 150 <= event.pos[0] <= 650:
                    if 200 <= event.pos[1] <= 250:
                        open_box("Drewniana Skrzynka")
                    elif 300 <= event.pos[1] <= 350:
                        open_box("Złota Skrzynka")
                    elif 400 <= event.pos[1] <= 450:
                        open_box("Boska Skrzynka")
                if back_button.collidepoint(event.pos):
                    mode = "main"
            elif mode == "choosing_mortar":
                for idx, mortar in enumerate(owned_mortars):
                    if 100 <= event.pos[0] <= 700 and 150 + idx * 40 <= event.pos[1] <= 190 + idx * 40:
                        choose_mortar(idx)
                        mode = "main"
            elif mode == "showing_unbox":
                mode = "main"
            elif mode == "upgrade_choice":
                if 200 <= event.pos[0] <= 600:
                    if 200 <= event.pos[1] <= 250:
                        apply_upgrade("szpachelka")
                    elif 300 <= event.pos[1] <= 350:
                        apply_upgrade("ubranie")
                    elif 400 <= event.pos[1] <= 450:
                        apply_upgrade("stawianie")
            elif mode == "level_up":
                mode = "main"

    if mode == "building_wall":
        if building_animation_frames:
            frame_count = len(building_animation_frames)
            elapsed = now - building_wall_timer
            index = int((elapsed / building_animation_duration) * frame_count)
            if index >= frame_count:
                mode = "main"
            else:
                screen.blit(building_animation_frames[index], (0, 0))
        else:
            draw_text("Stawianie muru...", 300, 250, YELLOW)

    elif mode == "main":
        pygame.draw.rect(screen, GREEN, brick_button, border_radius=10)
        draw_text("Postaw cegłę", brick_button.x + 20, brick_button.y + 10)

        pygame.draw.rect(screen, BLUE, box_button, border_radius=10)
        draw_text("Kup skrzynkę", box_button.x + 20, box_button.y + 10)

        pygame.draw.rect(screen, YELLOW, select_mortar_button, border_radius=10)
        draw_text("Wybierz zaprawę", select_mortar_button.x + 5, select_mortar_button.y + 10)

        draw_text(f"EXP: {exp}/{exp_to_next}", 50, 50)
        draw_text(f"Level: {level}", 50, 90)
        draw_text(f"Pieniądze: ${money}", 50, 130)
        draw_text(f"Zaprawa: {current_mortar}", 50, 170)

    elif mode == "choosing_box":
        draw_text("Wybierz skrzynkę:", 300, 100)
        draw_text("Drewniana Skrzynka - 50$", 250, 210, GREEN)
        draw_text("Złota Skrzynka - 150$", 250, 310, BLUE)
        draw_text("Boska Skrzynka - 500$", 250, 410, RED)
        pygame.draw.rect(screen, RED, back_button)
        draw_text("Wróć", back_button.x + 20, back_button.y + 10)

    elif mode == "choosing_mortar":
        draw_text("Wybierz zaprawę:", 300, 50)
        for idx, mortar in enumerate(owned_mortars):
            draw_text(f"{idx + 1}. {mortar}", 100, 150 + idx * 40)

    elif mode == "showing_unbox":
        draw_text(f"Nowa zaprawa: {last_unboxed_mortar}!", 250, 250, YELLOW)
        draw_text("Kliknij, aby kontynuować...", 250, 350)

    elif mode == "upgrade_choice":
        draw_text("LEVEL UP! Wybierz ulepszenie:", 200, 100)
        draw_text("Lepsza szpachelka (więcej exp $)", 200, 210)
        draw_text("Lepsze ubranie (tańsze skrzynki)", 200, 310)
        draw_text("Szybsze stawianie muru", 200, 410)

    elif mode == "level_up":
        draw_text(f"Wbijasz {level} poziom! Gratulacje!", 200, 250, YELLOW)
        if now - level_up_message_timer > 1500:
            mode = "main"

    pygame.display.flip()
    clock.tick(60)
