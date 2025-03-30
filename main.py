import pygame
import random
from model.Plant import PeaShooter, Plant, Sunflower, WallNut
from model.Position import Position
from model.Zombie import Zombie
from model.screen import Window, Eviron

pygame.init()
screen = pygame.display.set_mode((1300, 700))
running = True

# ---system---#
icon = pygame.image.load('assets/icons/pvzIcon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Plants vs Zombies')

# background
# grassField = pygame.transform.scale(pygame.image.load("assets/images/world.png"), (1152, 520))
grassField = pygame.image.load("assets/images/worldblur.png")

# --------image----
peaShooterImg = pygame.transform.scale(pygame.image.load("assets/models/peaShooter.png"), (80, 120))
zombieImg = pygame.transform.scale(pygame.image.load("assets/models/normalZombie.png"), (80, 120))
sunflowerImg = pygame.transform.scale(pygame.image.load("assets/models/sunflower.png"), (80, 120))
wallnutImg = pygame.transform.scale(pygame.image.load("assets/models/wallnut.png"), (80, 120))

# Grid settings
GRID_ROWS = 6
GRID_COLS = 9
CELL_WIDTH = 1152 // GRID_COLS
CELL_HEIGHT = 520 // GRID_ROWS
GRID_OFFSET_X = 1300 - 1152
GRID_OFFSET_Y = 700 - 520

# Store settings
STORE_HEIGHT = 100
store_peashooter = pygame.transform.scale(peaShooterImg, (60, 90))
store_sunflower = pygame.transform.scale(sunflowerImg, (60, 90))
store_wallnut = pygame.transform.scale(wallnutImg, (60, 90))
store_rect_peashooter = pygame.Rect(50, 20, 60, 90)
store_rect_sunflower = pygame.Rect(120, 20, 60, 90)
store_rect_wallnut = pygame.Rect(190, 20, 60, 90)

# Game resources
sun_points = 50
kill_count = 0
font = pygame.font.Font(None, 36)

ROW_POSITIONS = [43, 130, 217, 303, 390, 477]
# --------object-----
zombieList = []
plantList = []
peaList = []
selected_plant = None
#-----state variavles---------#
zombieBornRate = 5000
zombieHealth = 150

# ----Time---------
lastFrame = pygame.time.get_ticks()

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

# game loop
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if store_rect_peashooter.collidepoint(mouse_pos) and sun_points >= 100:
                selected_plant = PeaShooter(1, 100, Position(mouse_pos[0], mouse_pos[1]), 
                                          pygame.transform.scale(peaShooterImg, (50, 80)))
                sun_points -= 100
            elif store_rect_sunflower.collidepoint(mouse_pos) and sun_points >= 50:
                selected_plant = Sunflower(1, 50, Position(mouse_pos[0], mouse_pos[1]), 
                                         pygame.transform.scale(sunflowerImg, (50, 80)))
                sun_points -= 50
            elif store_rect_wallnut.collidepoint(mouse_pos) and sun_points >= 50:
                selected_plant = WallNut(1, 50, Position(mouse_pos[0], mouse_pos[1]), 
                                       pygame.transform.scale(wallnutImg, (50, 80)))
                sun_points -= 50
            elif selected_plant:
                snap_pos, grid_x, grid_y = get_closest_cell(mouse_pos[0], mouse_pos[1])
                if not is_cell_occupied(grid_x, grid_y):
                    selected_plant.position = snap_pos
                    if isinstance(selected_plant, PeaShooter):
                        selected_plant.image = peaShooterImg
                    elif isinstance(selected_plant, Sunflower):
                        selected_plant.image = sunflowerImg
                    elif isinstance(selected_plant, WallNut):
                        selected_plant.image = wallnutImg
                    plantList.append(selected_plant)
                selected_plant = None

    # Fill background
    screen.fill((165, 255, 255))
    screen.blit(grassField,(0,0))
    
    # Draw store area
    # pygame.draw.rect(screen, (200, 200, 200), (0, 0, 1300, STORE_HEIGHT))
    screen.blit(store_peashooter, (50, 20))
    screen.blit(store_sunflower, (120, 20))
    screen.blit(store_wallnut, (190, 20))
    
    # Draw sun points
    sun_text = font.render(f"Sun: {sun_points}", True, (255, 200, 0))
    screen.blit(sun_text, (300, 60))
    
    # Draw kill count in top right
    kill_text = font.render(f"Kills: {kill_count}", True, (200, 0, 0))
    screen.blit(kill_text, (1150, 60))
    
    # Draw game area
    # screen.blit(grassField, (GRID_OFFSET_X, GRID_OFFSET_Y))
    draw_grid()

    # Draw placed plants and handle their actions
    for plant in plantList[:]:
        plant.draw(screen)
        action_result = plant.shoot(current_time)
        if action_result is not None:
            if isinstance(action_result, int):
                sun_points += action_result
            elif hasattr(action_result, 'draw'):
                peaList.append(action_result)
    
    # Handle peas
    for pea in peaList[:]:
        pea.draw(screen)
        pea.move()
        pea_rect = pea.get_rect()
        for zombie in zombieList[:]:
            
            if zombie.position.x + 50 <= Eviron.position.startx:
                running = False
            
            zombie_rect = zombie.get_rect()
            if pea_rect.colliderect(zombie_rect):
                zombie.take_damage(pea.damage)
                peaList.remove(pea)
                if zombie.health <= 0:
                    zombieList.remove(zombie)
                    kill_count += 1
                    if kill_count == 15:
                        zombieBornRate = 3000
                    if kill_count == 30:
                        zombieHealth = 220
                        zombieBornRate = 1000
                break  # Exit zombie loop after collision
        else:  # Only check off-screen if no collision occurred
            if pea.position.x > Eviron.position.endx:
                peaList.remove(pea)

    # Draw selected plant following mouse
    if selected_plant:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected_plant.position = Position(mouse_x - 40, mouse_y - 60)
        selected_plant.draw(screen)

    # Handle zombies and plant interactions
    for zombie in zombieList[:]:
        zombie_is_colliding = False
        zombie_rect = zombie.get_rect()
        
        for plant in plantList[:]:
            plant_rect = plant.image.get_rect(topleft=(plant.position.x, plant.position.y))
            if zombie_rect.colliderect(plant_rect):
                zombie_is_colliding = True
                if zombie.attack(current_time, plant):
                    plantList.remove(plant)
                break
        
        if not zombie_is_colliding:
            zombie.move()
        zombie.draw(screen)

    # ----------spawning----------
    if current_time - lastFrame > zombieBornRate:
        row_y = random.choice(ROW_POSITIONS)
        zombieList.append(
            Zombie(1, zombieImg, Position(x=Eviron.position.endx, y=Eviron.setEnviLocY(Eviron(), row_y - 120)),zombieHealth))
        lastFrame = current_time
    
    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()