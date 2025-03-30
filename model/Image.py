import pygame

class Image:
    peaShooter = None
    wallnute = None
    zoombie = None
    pea = None
    sunflower = None

    @staticmethod
    def load_images():
        # Load and scale images
        Image.peaShooter = pygame.transform.scale(pygame.image.load("assets/models/peaShooter.png"), (80, 120))
        Image.wallnute = pygame.transform.scale(pygame.image.load("assets/models/wallNut.png"), (80, 120))
        Image.zoombie = pygame.transform.scale(pygame.image.load("assets/models/normalZombie.png"), (80, 120))
        Image.pea = pygame.transform.scale(pygame.image.load("assets/images/pea.webp"), (50, 50))
        Image.sunflower = pygame.transform.scale(pygame.image.load("assets/models/sunflower.png"), (80, 120))