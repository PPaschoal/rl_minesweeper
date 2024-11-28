import torch 
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class CampoMinadoModel(nn.Module):
    def __init__(self,x,y,n_camadas,tamanho_saida):
        super().__init__()
        
        inputs = x * y * n_camadas
        
        self.linear1 = nn.Linear(inputs,256)
        self.linear2 = nn.Linear(256,tamanho_saida)
        
    def forward(self,x):
        x = torch.reshape(x,(-1,))
        
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
class QTrainer:
    def __init__(self,model,lr,gamma):
        self.lr = lr
        self.gamma = gamma
        self.modelo = model
        self.otimizador =  optim.Adam(model.parameters(), lr=self.lr)
        self.criterio = nn.MSELoss()
        
    def passo_treino(self,estado,acao,recompensa,prox_estado,fim_de_jogo):
        estado = torch.tensor(estado,dtype=torch.float)
        prox_estado = torch.tensor(prox_estado,dtype=torch.float)
        acao = torch.tensor(acao,dtype=torch.long)
        recompensa = torch.tensor(recompensa,dtype=torch.float)
        
        if len(estado.shape) == 3:
            estado = torch.unsqueeze(estado,0)
            prox_estado = torch.unsqueeze(prox_estado,0)
            acao = torch.unsqueeze(acao,0)
            recompensa = torch.unsqueeze(recompensa,0)
            fim_de_jogo = (fim_de_jogo, )
        
        pred = self.modelo(estado)
        
        alvo = pred.clone()
        
        for i in range(len(fim_de_jogo)):
            Q_novo = recompensa[i]
            if not fim_de_jogo[i]:
                Q_novo = recompensa[i] + self.gamma * torch.max(self.modelo(prox_estado[i]))
            
            
            alvo[torch.argmax(acao).item()] = Q_novo
        
        self.otimizador.zero_grad()
        perda = self.criterio(alvo,pred)
        perda.backward()
        
        self.otimizador.step()