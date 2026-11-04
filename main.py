import pygame
import random
import json
from pathlib import Path
from platformdirs import user_data_path

save_data = {}


pygame.init()
clock = pygame.time.Clock()

sprite_frame_size = pygame.Vector2(16, 16)

window = pygame.display.set_mode((800, 600))
window.fill((0, 0, 0))
pygame.display.set_caption("Fruit rush")

data = user_data_path(pygame.display.get_caption()[0])
data.mkdir(parents=True, exist_ok=True)
save_file = (data/"save.dat")

HIGH_SCORE_KEY = "HighScore"

def to_json(dict_str: str):
    try:
        return json.loads(dict_str)
    except json.JSONDecodeError:
        return None


def init_default_save():
    save_data.get(HIGH_SCORE_KEY, int(0))


if (not save_file.exists()):
    init_default_save()
    save_file.write_text(json.dumps(save_data, indent=2))
if to_json(save_file.read_text()) == None:
    init_default_save()
    save_file.write_text(json.dumps(save_data, indent=2))
save_data = json.loads(save_file.read_text())

def save_score(score: int):
    if save_data[HIGH_SCORE_KEY] < score:
        save_data[HIGH_SCORE_KEY] = score
        save_data = json.loads(save_file.read_text())

score = 0


player = pygame.surface.Surface((100, 100))
player.fill((255, 255, 255))
player = pygame.image.load("Assets/Sprites/Fruit rush.png").subsurface((0, 0, sprite_frame_size.x, sprite_frame_size.y))
player = pygame.transform.scale(player, (128, 128))


falling_fruit = pygame.surface.Surface((100, 100))
falling_fruit.fill((255, 255, 255))
falling_fruit = pygame.image.load("Assets/Sprites/Fruit rush.png").subsurface((random.randint(1, 2)*16, 0, sprite_frame_size.x, sprite_frame_size.y))
falling_fruit = pygame.transform.scale(falling_fruit, (128, 128))

bg = pygame.surface.Surface(window.size)
bg.fill((255, 255, 255))
bg = pygame.image.load("Assets/Sprites/BG fruit rush.png").subsurface((0, 0, 100, 75))
bg = pygame.transform.scale(bg, window.size)

tree = pygame.surface.Surface(window.size)
tree.fill((255, 255, 255))
tree = pygame.image.load("Assets/Sprites/BG fruit rush.png").subsurface((100, 0, 100, 75))
tree = pygame.transform.scale(tree, window.size)

player_pos = pygame.Vector2(336, 400)
player_velocity = pygame.Vector2()

falling_fruit_pos = pygame.Vector2(random.randint(10, round(window.width-falling_fruit.get_rect().right-10)), -16)
falling_fruit_velocity = pygame.Vector2(0, 400)

tree_pos = pygame.Vector2()

dt = 0

SPEED = 600
# print(window.width)


def checkCollision():
    return(
        (int(player_pos.x+20) <= int(falling_fruit_pos.x+falling_fruit.width) and 
        int(falling_fruit_pos.x-20) <= int(player.width+player_pos.x)) and
        (int(player_pos.y) <= int(falling_fruit_pos.y+falling_fruit.height-150) and
        int(falling_fruit_pos.y) <= int(player_pos.y+player.height))
    )

while True:
    # Inpute

    #Handle exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player_velocity.x != 0:
                    player_velocity.x = -player_velocity.x
                else:
                    player_velocity.x = SPEED
    if player.get_rect().right+player_pos.x >= window.width:
        player_velocity.x = -SPEED
    elif player_pos.x <= 0:
        player_velocity.x = SPEED

    if falling_fruit_pos.y >= window.height:
        if checkCollision():
            score += 1
        falling_fruit_pos = pygame.Vector2(random.randint(10, round(window.width-falling_fruit.get_rect().right-10)), -100)
        falling_fruit = pygame.image.load("Assets/Sprites/Fruit rush.png").subsurface((random.randint(1, 2)*16, 0, sprite_frame_size.x, sprite_frame_size.y))
        falling_fruit = pygame.transform.scale(falling_fruit, (128, 128))

 
    #Output
    window.fill((255, 255, 255))


    #draw sprites
    player_pos.x += player_velocity.x*dt
    player_pos.y += player_velocity.y*dt
    falling_fruit_pos.x += falling_fruit_velocity.x*dt
    falling_fruit_pos.y += falling_fruit_velocity.y*dt

    window.blit(bg, (0, 0))
    window.blit(tree, tree_pos)
    window.blit(falling_fruit, falling_fruit_pos)
    window.blit(player, player_pos)

    pygame.display.flip()
    dt = clock.tick_busy_loop(60)/1000