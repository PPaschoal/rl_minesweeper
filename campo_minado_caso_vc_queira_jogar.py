import pygame
from game import Engine
from graficos import Graficos
from pygame.locals import *
from sys import exit

class Game(Engine,Graficos):
    def __init__(self):
        Engine.__init__(self)
        pygame.init()
        self.largura = self.x * 16
        self.altura = self.y * 16
        self.tela = pygame.display.set_mode((self.largura,self.altura))
        pygame.display.set_caption('Campo Minado')
        
        
    def play(self):
        while not self.jogo_terminou:
            self.rodar()
            if self.jogo_terminou:
                self.reset()
        
    def rodar(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONUP:
                x,y = event.pos
                x = x//16
                y = y//16
                if self.campo_jogo[y][x] == 10:
                    if event.button == 1:
                        self.abrirCelula(x,y)
                    elif event.button == 3:
                        self.colocarBandeira(x,y)
                elif self.campo_jogo[y][x] in range(1,9):
                    if event.button == 1:
                        self.abrirMultiplasCelulas(x,y)
                elif self.campo_jogo[y][x] == 12:
                    if event.button == 3:
                        self.removerBandeira(x,y)
                    
                self.jogo_terminou,self.bomba_explodiu = self.estadoJogo()
                
                if self.jogo_terminou:
                    self.gameOver()
                    if self.bomba_explodiu:
                        print("perdeste")
                    else:
                        print("ganhaste")
        
        self.carregarCampo()        
        pygame.display.update()

    def reset(self):
        while self.jogo_terminou:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONUP:
                    print("pass")
                    Engine.__init__(self)

jogo = Game()
jogo.play()
