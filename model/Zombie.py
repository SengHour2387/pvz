class Zombie:
    def __init__(self, id, image, position , health = 150):
        self.id = id
        self.image = image
        self.position = position
        self.speed = 1
        self.health = health  # Now an instance variable
        self.attack_damage = 20  # Damage dealt to plants
        self.attack_rate = 1  # Attacks per second
        self.last_attack = 0  # Track last attack time
    
    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))
        
    def move(self):
        self.position.x -= self.speed 
        
    def take_damage(self, damage):
        self.health -= damage
        
    def get_rect(self):
        return self.image.get_rect(topleft=(self.position.x, self.position.y))
    
    def attack(self, current_time, plant):
        # Attack plant if cooldown has passed
        if current_time - self.last_attack >= 2000 / self.attack_rate:
            plant.take_damage(self.attack_damage)
            self.last_attack = current_time
            return plant.health <= 0  # Return True if plant should be removed
        return False