# Importar as bibliotecas
import sys
import pygame

# Importar os módulos criados
from level import Level
from configuracoes import *
from overworld import Overworld


# Criar a classe do jogo
class Jogo:
    def __init__(self):
        # Configurações iniciais de "Overworld()"
        self.estado = 'overworld'  # trocar entre o Overworld e o Level
        self.level_final = 0
        self.overworld = Overworld(0, self.level_final, tela, self.criar_level)

    def criar_level(self, level_atual):
        """Função responsável por criar o level"""
        self.level = Level(level_atual, tela, self.criar_overworld)
        self.estado = 'level'

    def criar_overworld(self, level_atual, novo_level_final):
        """Função responsável por criar o Overworld depois de sair de um level"""
        if novo_level_final > self.level_final:
            self.level_final = novo_level_final  # isso ocorre somente quando o jogdor passa de level
        self.overworld = Overworld(level_atual, self.level_final, tela, self.criar_level)
        self.estado = 'overworld'

    def executar(self):
        """Função responsável pela execução do jogo"""
        if self.estado == 'overworld':
            # Executar o mapa do Overworld
            self.overworld.executar()
        else:
            # Executar o mapa do Level
            self.level.executar()


# Configurações iniciais do Pygame
pygame.init()  # iniciar o Pygame
relogio = pygame.time.Clock()  # usar como o FPS
tela = pygame.display.set_mode((LARGURA, ALTURA))  # criar a tela
jogo = Jogo()  # chamar a classe responsável por executar o jogo

# Game Loop
while True:
    # Eventos de interação com o Pygame
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            # Fechar a tela quando apertar "X"
            pygame.quit()
            sys.exit()

    # Preencher a tela
    tela.fill('grey')

    # Iniciar o jogo
    jogo.executar()

    # Atualizar a tela
    pygame.display.update()

    # FPS
    relogio.tick(60)
