import pygame

class Game:
    zombieList = []
    plantList = []
    def __init__(self,player):
        self.player = player

    def addPlant(self,plant):
        self.plantList.append(plant)
        
    def removePlant(self,plant):
        self.plantList.remove(plant)
    def addZombie(self,zombie):
        self.zombieList.append(zombie)
    def removeZombie(self,zombie):
        self.zombieList.remove(zombie)
        