import pygame
import random
from model.Plant import PeaShooter, Plant, Sunflower, WallNut
from model.Position import Position
from model.Zombie import Zombie
from model.screen import Window, Eviron
from model.Image import Image

pygame.init()
screen = pygame.display.set_mode((1300, 700))
running = True
game_over = False

# Load images from Image class
Image.load_images()

# ---system---#
icon = pygame.image.load('assets/icons/pvzIcon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Plants vs Zombies')

grassField = pygame.image.load("assets/images/worldblur.png")

GRID_ROWS = 6
GRID_COLS = 9
CELL_WIDTH = 1152 // GRID_COLS
CELL_HEIGHT = 520 // GRID_ROWS
GRID_OFFSET_X = 1300 - 1152
GRID_OFFSET_Y = 700 - 520

STORE_HEIGHT = 100
store_peashooter = pygame.transform.scale(Image.peaShooter.current_frame, (60, 90))
store_sunflower = pygame.transform.scale(Image.sunflower.current_frame, (60, 90))
store_wallnut = pygame.transform.scale(Image.wallnute, (60, 90))
store_rect_peashooter = pygame.Rect(50, 20, 60, 90)
store_rect_sunflower = pygame.Rect(120, 20, 60, 90)
store_rect_wallnut = pygame.Rect(190, 20, 60, 90)

sun_points = 50
kill_count = 0
font = pygame.font.Font(None, 36)

try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read().strip())
except (FileNotFoundError, ValueError):
    high_score = 0

ROW_POSITIONS = [43, 130, 217, 303, 390, 477]

zombieList = []
plantList = []
peaList = []
selected_plant = None

zombieBornRate = 10000
zombieHealth = 150
sun_rate = 4
lastFrame = pygame.time.get_ticks()

# Define functions before the game loop
def draw_grid():
    for row in range(GRID_ROWS + 1):
        pygame.draw.line(screen, (200, 200, 200), 
                        (GRID_OFFSET_X, GRID_OFFSET_Y + row * CELL_HEIGHT),
                        (GRID_OFFSET_X + GRID_COLS * CELL_WIDTH, GRID_OFFSET_Y + row * CELL_HEIGHT))
    for col in range(GRID_COLS + 1):
        pygame.draw.line(screen, (200, 200, 200),
                        (GRID_OFFSET_X + col * CELL_WIDTH, GRID_OFFSET_Y),
                        (GRID_OFFSET_X + col * CELL_WIDTH, GRID_OFFSET_Y + GRID_ROWS * CELL_HEIGHT))

def is_cell_occupied(grid_x, grid_y):
    for plant in plantList:
        plant_grid_x = (plant.position.x - GRID_OFFSET_X + 40) // CELL_WIDTH
        plant_grid_y = (plant.position.y - GRID_OFFSET_Y + 60) // CELL_HEIGHT
        if plant_grid_x == grid_x and plant_grid_y == grid_y:
            return True
    return False

def get_closest_cell(mouse_x, mouse_y):
    grid_x = max(0, min(GRID_COLS - 1, (mouse_x - GRID_OFFSET_X) // CELL_WIDTH))
    grid_y = max(0, min(GRID_ROWS - 1, (mouse_y - GRID_OFFSET_Y) // CELL_HEIGHT))
    return Position(
        x=GRID_OFFSET_X + grid_x * CELL_WIDTH + CELL_WIDTH // 2 - 40,
        y=GRID_OFFSET_Y + grid_y * CELL_HEIGHT + CELL_HEIGHT // 2 - 80
    ), grid_x, grid_y

def reset_game():
    global sun_points, kill_count, zombieList, plantList, peaList, selected_plant, zombieBornRate, zombieHealth, lastFrame
    sun_points = 50
    kill_count = 0
    zombieList = []
    plantList = []
    peaList = []
    selected_plant = None
    zombieBornRate = 10000
    zombieHealth = 150
    lastFrame = pygame.time.get_ticks()

clock = pygame.time.Clock()

# Game loop
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            if store_rect_peashooter.collidepoint(mouse_pos) and sun_points >= 100:
                selected_plant = PeaShooter(1, 100, Position(mouse_pos[0], mouse_pos[1]), 
                                          pygame.transform.scale(Image.peaShooter.current_frame, (50, 80)))
                sun_points -= 100
            elif store_rect_sunflower.collidepoint(mouse_pos) and sun_points >= 50:
                selected_plant = Sunflower(1, 50, Position(mouse_pos[0], mouse_pos[1]), 
                                         pygame.transform.scale(Image.sunflower.current_frame, (50, 80)),sun_rate)
                sun_points -= 50
            elif store_rect_wallnut.collidepoint(mouse_pos) and sun_points >= 50:
                selected_plant = WallNut(1, 50, Position(mouse_pos[0], mouse_pos[1]), 
                                       pygame.transform.scale(Image.wallnute, (50, 80)))
                sun_points -= 50
            elif selected_plant:
                snap_pos, grid_x, grid_y = get_closest_cell(mouse_pos[0], mouse_pos[1])
                if not is_cell_occupied(grid_x, grid_y):
                    selected_plant.position = snap_pos
                    if isinstance(selected_plant, PeaShooter):
                        selected_plant.image = Image.peaShooter
                    elif isinstance(selected_plant, Sunflower):
                        selected_plant.image = Image.sunflower
                    elif isinstance(selected_plant, WallNut):
                        selected_plant.image = Image.wallnute
                    plantList.append(selected_plant)
                selected_plant = None
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                reset_game()
                game_over = False

    if not game_over:
        screen.blit(grassField, (0, 0))
        screen.fill((165, 255, 255), (0, 0, 1300, STORE_HEIGHT))
        
        screen.blit(store_peashooter, (50, 20))
        screen.blit(store_sunflower, (120, 20))
        screen.blit(store_wallnut, (190, 20))
        
        sun_text = font.render(f"Sun: {sun_points}", True, (255, 200, 0))
        screen.blit(sun_text, (300, 60))
        zomebie_text = font.render(f"Zombie Health: {zombieHealth}", True, (0, 200, 0))
        screen.blit(zomebie_text, (800, 60))
        kill_text = font.render(f"Kills: {kill_count}", True, (200, 0, 0))
        screen.blit(kill_text, (1150, 60))
        
        draw_grid()

        for plant in plantList[:]:
            plant.draw(screen)
            action_result = plant.shoot(current_time,sun_rate)
        
            if action_result is not None:
                if isinstance(action_result, int):
                    sun_points += action_result
                elif hasattr(action_result, 'draw'):
                    peaList.append(action_result)
        
        for pea in peaList[:]:
            pea.draw(screen)
            pea.move()
            pea_rect = pea.get_rect()
            for zombie in zombieList[:]:
                if zombie.position.x + 50 <= Eviron.position.startx:
                    game_over = True
        
                zombie_rect = zombie.get_rect()
                if pea_rect.colliderect(zombie_rect):
                    zombie.take_damage(pea.damage)
                    peaList.remove(pea)
                    if zombie.health <= 0:
                        zombieList.remove(zombie)
                        kill_count += 1
                        if kill_count == 1:
                            sun_rate = 5
                        if kill_count == 2:
                            sun_rate = 10
                            zombieBornRate = 8000
                            zombieHealth = 200
                        if kill_count == 3:
                            sun_rate = 15
                            zombieHealth = 250
                            zombieBornRate = 7000
                        if kill_count == 10:
                            sun_rate = 18
                            zombieBornRate = 6000
                            zombieHealth = 320
                        if kill_count == 15:
                            sun_rate = 20
                            zombieHealth = 350
                            zombieBornRate = 5000
                        if kill_count == 20:
                            sun_rate = 25
                            zombieHealth = 380
                        if kill_count == 25:
                            sun_rate = 25
                            zombieBornRate = 4000
                            zombieHealth = 410
                        if kill_count == 30:
                            sun_rate = 25	
                            zombieBornRate = 3000
                            zombieHealth = 450
                            
                    break
            else:
                if pea.position.x > Eviron.position.endx:
                    peaList.remove(pea)

        if selected_plant:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected_plant.position = Position(mouse_x - 40, mouse_y - 60)
            selected_plant.draw(screen)

        for zombie in zombieList[:]:
            zombie_is_colliding = False
            zombie_rect = zombie.get_rect()
 
            for plant in plantList[:]:
                plant_rect = plant.get_rect()
                if zombie_rect.colliderect(plant_rect):
                    zombie_is_colliding = True
                    zombie.setImage(Image.zoombieEat)
                    if zombie.attack(current_time, plant):
                        plantList.remove(plant)
                    break

            if not zombie_is_colliding:
                zombie.setImage(Image.zoombie)
                zombie.move()
            zombie.draw(screen)

        if current_time - lastFrame > zombieBornRate:
            row_y = random.choice(ROW_POSITIONS)
            zombieList.append(
                Zombie(1, Image.zoombie, Position(x=Eviron.position.endx, y=Eviron.setEnviLocY(Eviron(), row_y - 120)), zombieHealth))
            lastFrame = current_time

    else:
        if kill_count > high_score:
            high_score = kill_count
            with open("highscore.txt", "w") as file:
                file.write(str(high_score))

        screen.fill((0, 0, 0))
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        restart_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
        score_text = font.render(f"Score: {kill_count}", True, (255, 255, 0))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
        
        screen.blit(game_over_text, (550, 250))
        screen.blit(restart_text, (450, 350))
        screen.blit(score_text, (550, 450))
        screen.blit(high_score_text, (550, 500))

    pygame.display.update()
    clock.tick(60)

pygame.quit()