import pygame
from .Image import Image
class Zombie:
    def __init__(self, id, image, position, health=150):
        self.id = id
        self.image = image  # Can be pygame.Surface or AnimatedImage
        self.position = position
        self.speed = 1/3
        self.health = health
        self.attack_damage = 20
        self.attack_rate = 1  # Attacks per second
        self.last_attack = 0  # Track last attack time

    def draw(self, screen):
        # Check if image is a Surface or AnimatedImage
        if isinstance(self.image, pygame.Surface):
            screen.blit(self.image, (self.position.x, self.position.y + 40))
        else:  # AnimatedImage
            screen.blit(self.image.current_frame, (self.position.x, self.position.y + 40))
        
    def move(self):
        self.position.x -= self.speed 
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 10:
            self.image = Image.zoombieDie
        
    def get_rect(self):
        # Return rect based on image type
        if isinstance(self.image, pygame.Surface):
            return self.image.get_rect(topleft=(self.position.x, self.position.y))
        else:  # AnimatedImage
            return self.image.current_frame.get_rect(topleft=(self.position.x, self.position.y))
        
    def setImage(self, image):
        self.image = image
        
    def attack(self, current_time, plant):
        if current_time - self.last_attack >= 2000 / self.attack_rate:
            plant.take_damage(self.attack_damage)
            self.last_attack = current_time
            return plant.health <= 0  # Return True if plant should be removed
        return False