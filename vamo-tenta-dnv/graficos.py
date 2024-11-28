import pygame
import os

class Graficos:
    def carregarCampo(self):
        for i in range(self.y):
            for j in range(self.x):
                celula =self.campo_jogo[i][j]
                img = pygame.image.load(os.path.join("assets", f"{celula}.png"))
                x = j*16
                y = i*16
                self.tela.blit(img,(x,y))