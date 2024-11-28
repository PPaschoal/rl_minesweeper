from random import randint

class Engine:
    def __init__(self):
        self.x = 30
        self.y = 15
        self.num_bombas = 99
        self.bombas_restantes = self.num_bombas
        self.campo_resposta = self.criarCampoResposta()
        self.campo_jogo = self.criarCampoJogo()
        self.jogo_terminou = False
        self.bomba_explodiu = False


    def criarCampoResposta(self):
        campo = list()
        for _ in range(self.y):
            campo.append([0]*self.x)
            
        campo = self.colocarBombas(campo)
        campo = self.inserirQtdBombas(campo)
        return campo
        
    def criarCampoJogo(self):
        campo = list()
        for _ in range(self.y):
            campo.append([10]*self.x)
        return campo
    
    def vizinhos(self,i,j):
        vizinhos_valores = list()
        for y in [-1,1,0]:
            for x in [-1,1,0]:
                if y != 0 or x != 0:
                    celula_x = j + x
                    celula_y = i + y
                    if 0<=celula_y<self.y and 0<=celula_x<self.x:
                        vizinhos_valores.append((celula_y,celula_x))
        return vizinhos_valores
    
    def colocarBombas(self,campo):
        for _ in range(self.num_bombas):
            while True:
                bomba_x = randint(0,29)
                bomba_y = randint(0,14)
                if campo[bomba_y][bomba_x] != 11:
                    break
                
            campo[bomba_y][bomba_x] = 11
        return campo
        
    def inserirQtdBombas(self,campo):
        for i in range(self.y):
            for j in range(self.x):
                qtd_bombas = 0
                if campo[i][j] == 11:
                    continue
                for vizinho in self.vizinhos(i,j):
                    celula_y,celula_x = vizinho
                    if campo[celula_y][celula_x] == 11:
                        qtd_bombas += 1
                campo[i][j] = qtd_bombas
        return campo

    def abrirCelula(self,x,y):
        valor_celula = self.campo_resposta[y][x]
        self.campo_jogo[y][x] = valor_celula
        if valor_celula == 0:
            for vizinho in self.vizinhos(y,x):
                celula_y,celula_x = vizinho
                if self.campo_jogo[celula_y][celula_x] == 10:
                    self.abrirCelula(celula_x,celula_y)
                
    def colocarBandeira(self,x,y):
        self.campo_jogo[y][x] = 12
        self.bombas_restantes -= 1

    def removerBandeira(self,x,y):
        self.campo_jogo[y][x] = 10
        self.bombas_restantes += 1

    def abrirMultiplasCelulas(self,x,y):
        qtd_bombas = self.campo_jogo[y][x]
        coordenadas_vizinhos = self.vizinhos(y,x)
        num_bandeiras = 0
        celulas_n_abertas = [(x,y) for x,y in coordenadas_vizinhos if self.campo_jogo[x][y] == 10]

        for i,j in coordenadas_vizinhos:
            val = self.campo_jogo[i][j]
            if val == 12:
                num_bandeiras += 1

            
        if qtd_bombas == num_bandeiras:
            for i,j in celulas_n_abertas:
                self.abrirCelula(j,i)
                
    def estadoJogo(self):
        celulas_restantes = 0
        bombas = 0
        for i in range(self.y):
            celulas_restantes += self.campo_jogo[i].count(10)
            bombas += self.campo_jogo[i].count(11)
            if bombas > 0:
                return True,True
        
        if celulas_restantes == self.bombas_restantes:
            return True,False
        else:
            return False,False
        
        
    def gameOver(self):
        for i in range(self.y):
            for j in range(self.x):
                val = self.campo_resposta[i][j]
                if (val == 11 and self.bomba_explodiu) and self.campo_jogo[i][j] == 10:
                    self.campo_jogo[i][j] = 11
                elif val == 11 and not self.bomba_explodiu:
                    self.campo_jogo[i][j] = 12
                if val != 11 and self.campo_jogo[i][j] == 12:
                    self.campo_jogo[i][j] = 13

