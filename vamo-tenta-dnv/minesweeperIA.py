import pygame
from game import Engine
from graficos import Graficos
from pygame.locals import *
from sys import exit

class MinesweeperAI(Engine,Graficos):
    def __init__(self):
        Engine.__init__(self)
        pygame.init()
        self.largura = self.x * 16
        self.altura = self.y * 16
        self.tela = pygame.display.set_mode((self.largura,self.altura))
        pygame.display.set_caption('Campo Minado')
        self.frame_iteration = 0
        self.carregarCampo()
        pygame.display.update()
        
    def play(self):
        while not self.jogo_terminou:
            self.rodar()
            if self.jogo_terminou:
                self.reset()
        
    def rodar(self,acoes):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        recompensa = 0
        x = acoes[0]
        y = acoes[1]
        acao = acoes[2]
        
        qtd_celulas_antigo = [1 if self.campo_jogo[y][x] == 10 else 0 for y in range(self.y) for x in range(self.x)].count(1)
        
        if self.campo_jogo[y][x] == 10:
            if acao == 1:
                self.abrirCelula(x,y)
            else:
                self.colocarBandeira(x,y)
                recompensa -= 1
        elif self.campo_jogo[y][x] in range(1,9):
            if acao == 1:
                self.abrirMultiplasCelulas(x,y)
        elif self.campo_jogo[y][x] == 12:
            self.removerBandeira(x,y)
            
        qtd_celulas_novo = [1 if self.campo_jogo[y][x] == 10 else 0 for y in range(self.y) for x in range(self.x)].count(1)
        
        delta = qtd_celulas_antigo - qtd_celulas_novo
            
        if delta <= 0:
            recompensa = -1
        else:
            
            recompensa += 1 * delta
                    
        self.jogo_terminou,self.bomba_explodiu = self.estadoJogo()
                
        if self.frame_iteration > (self.x*self.y - qtd_celulas_novo) + 10:
            self.jogo_terminou = True
            self.bomba_explodiu = True
        
        if self.jogo_terminou:
            self.gameOver()
            if self.bomba_explodiu:
                recompensa = -100
            else:
                recompensa = 100+self.x*self.y
        
        self.carregarCampo()        
        pygame.display.update()
        
        
        
        return recompensa,self.jogo_terminou

    def reset(self):
        Engine.__init__(self)
        self.carregarCampo()
        pygame.display.update()
        self.frame_iteration = 0
