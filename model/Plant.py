from .Pea import Pea
import pygame
import copy

class Plant:
    def __init__(self, id, price, position, image, health=100):
        self.id = id
        self.price = price
        self.position = position
        self.image = image  # Can be pygame.Surface or AnimatedImage
        self.health = health
    
    def draw(self, screen):
        # Check if image is a Surface or AnimatedImage
        if isinstance(self.image, pygame.Surface):
            screen.blit(self.image, (self.position.x, self.position.y))
        else:  # AnimatedImage
            screen.blit(self.image.current_frame, (self.position.x, self.position.y))
    
    def get_rect(self):
        # Return rect based on image type
        if isinstance(self.image, pygame.Surface):
            rect = self.image.get_rect(topleft=(self.position.x, self.position.y))
            rect.height = 60
            return rect
        else:  # AnimatedImage
            rect = self.image.current_frame.get_rect(topleft=(self.position.x, self.position.y))
            rect.height = 60
            return rect
    
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
    
    def shoot(self, current_time,sunRate):
        if current_time - self.last_shot >= 1000 / self.fire_rate:
            pea_position = copy.deepcopy(self.position)
            bullet = Pea(position=pea_position, damage=self.damage)
            self.last_shot = current_time
            return bullet
        return None

class WallNut(Plant):
    def __init__(self, id, price, position, image, health=400):
        super().__init__(id, price, position, image, health)
    
    def draw(self, screen):
        super().draw(screen)
    
    def shoot(self, current_time,sunRate):
        return None

class Sunflower(Plant):
    def __init__(self, id, price, position, image, sun_rate,health=100):
        super().__init__(id, price, position, image, health)
        self.sun_rate = sun_rate # Generate sun every 5 seconds
        self.last_sun = 0  # Track last sun generation time
        self.sun_value = 25  # Amount of sun points generated
    
    def draw(self, screen):
        super().draw(screen)
    
    def shoot(self, current_time,sunRate):
        if current_time - self.last_sun >= 1000 * sunRate:
            self.last_sun = current_time
            return self.sun_value
        return None