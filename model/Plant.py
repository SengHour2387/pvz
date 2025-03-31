# model/Plant.py
from .Pea import Pea
import pygame
import copy

class Plant:
    def __init__(self, id, price, position, image, health=100):
        self.id = id
        self.price = price
        self.position = position
        self.image = image
        self.health = health
    
    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return f"{self.id} has withered away!"
        return f"{self.id} health: {self.health}"

class PeaShooter(Plant):
    def __init__(self, id, price, position, image, health=100):
        super().__init__(id, price, position, image, health)
        self.damage = 10
        self.range = 100
        self.fire_rate = 1  # Shots per second
        self.last_shot = 0  # Track last shot time
    
    def draw(self, screen):
        super().draw(screen)
    
    def shoot(self, current_time):
        # Implement a firing cooldown based on fire_rate
        if current_time - self.last_shot >= 1000 / self.fire_rate:
            pea_position = copy.deepcopy(self.position)
            bullet = Pea(position=pea_position, damage=self.damage)
            self.last_shot = current_time
            return bullet
        return None

class WallNut(Plant):
    def __init__(self, id, price, position, image, health=400):  # Higher health as a defensive plant
        super().__init__(id, price, position, image, health)
    
    def draw(self, screen):
        super().draw(screen)
    
    def shoot(self, current_time):
        # WallNut doesn't shoot, so always return None
        return None

class Sunflower(Plant):
    def __init__(self, id, price, position, image, health=100):
        super().__init__(id, price, position, image, health)
        self.sun_rate = 3  # Generate sun every 3 seconds
        self.last_sun = 0  # Track last sun generation time
        self.sun_value = 25  # Amount of sun points generated
    
    def draw(self, screen):
        super().draw(screen)
    
    def shoot(self, current_time):
        # Sunflower generates sun instead of shooting
        if current_time - self.last_sun >= 1000 * self.sun_rate:
            self.last_sun = current_time
            return self.sun_value  # Return sun points instead of a bullet
        return None
