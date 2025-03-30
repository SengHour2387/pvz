# model/Pea.py
import pygame
# from .Position import Position

class Pea:
    def __init__(self, position, damage):
        self.position = position
        self.damage = damage
        self.speed = 5
        self.image = pygame.transform.scale(pygame.image.load("assets/images/pea.webp"),(50,50))
    
    def draw(self, screen):
        screen.blit(self.image, (self.position.x + 50, self.position.y + 15))
    
    def move(self):
        self.position.x += self.speed
    def get_rect(self):
        # Return a Rect based on the position and image size
        return self.image.get_rect(topleft=(self.position.x, self.position.y + 15))