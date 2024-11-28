import torch
import random
import numpy as np
from collections import deque
from minesweeperIA import MinesweeperAI
from modelo import CampoMinadoModel,QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agente:
    def __init__(self,x,y):
        self.n_jogos = 0
        self.epsilon = 0 #definir rng
        self.gamma = 0.9
        self.memoria = deque(maxlen=MAX_MEMORY)
        outputs = x*y*2
        self.modelo = CampoMinadoModel(x,y,10,outputs)
        self.trainer = QTrainer(self.modelo,lr=LR,gamma=self.gamma)
        

        
        
    def estados(self,jogo):
        estados = list()
        for i in [1,2,3,4,5,6,7,8,10,12]:
            estadoI = np.array([[1 if jogo.campo_jogo[y][x] == i else 0 for x in range(jogo.x)] 
                            for y in range(jogo.y)])
            estados.append(estadoI)
        
        return np.array(estados, dtype=int)
            
    def lembrar(self,estado,acao,recompensa,prox_estado,fim_de_jogo):
        self.memoria.append((estado,acao,recompensa,prox_estado,fim_de_jogo))
    
    def memoria_longo_prazo(self):
        if len(self.memoria) > BATCH_SIZE:
            pequena_amostra = random.sample(self.memoria,BATCH_SIZE)
        else:
            pequena_amostra = self.memoria
        
        # estados,acoes,recompensas,prox_estados,fim_de_jogos = zip(*pequena_amostra)
        # self.trainer.passo_treino(estados,acoes,recompensas,prox_estados,fim_de_jogos)
        for estado,acao,recompensa,prox_estado,fim_de_jogo in pequena_amostra:
            self.trainer.passo_treino(estado,acao,recompensa,prox_estado,fim_de_jogo)
        
        
    def memoria_curto_prazo(self,estado,acao,recompensa,prox_estado,fim_de_jogo):
        self.trainer.passo_treino(estado,acao,recompensa,prox_estado,fim_de_jogo)
    
    def get_acao(self,estado,largura,altura):
        self.epsilon = 80 - self.n_jogos
        
        if random.randint(0,200) < self.epsilon:
            x = random.randint(0,largura-1)
            y = random.randint(0,altura-1)
            acao = random.randint(0,1)
        else:
            estado0 = torch.tensor(estado, dtype=torch.float)
            previsao = self.modelo(estado0)
            indice = torch.argmax(previsao).item()
            
            acao = indice % 2
            x = (indice // 2) % largura
            y = indice // (2 * largura)
                       
        acoes = [x,y,acao]
        return acoes
            
        
    
def treino():
    
    jogo = MinesweeperAI()
    agente = Agente(jogo.x,jogo.y)
    while True:
        estado_antigo = agente.estados(jogo)
        
        acao = agente.get_acao(estado_antigo,jogo.x,jogo.y)
        
        recompensa,fim_de_jogo = jogo.rodar(acao)
        
        estado_novo = agente.estados(jogo)
        
        agente.memoria_curto_prazo(estado_antigo,acao,recompensa,estado_novo,fim_de_jogo)
        
        agente.lembrar(estado_antigo,acao,recompensa,estado_novo,fim_de_jogo)
        
        if fim_de_jogo:
            jogo.reset()
            agente.n_jogos += 1
            agente.memoria_longo_prazo()
            
            print()
            print(f"Jogo:{agente.n_jogos}:")
            print(f"Recompensa:{recompensa}")
            print(f"Ultima ação:{acao}")
            
        
            
if __name__ == '__main__':
    treino()