# Importar as bibliotecas
import sys
import pygame

# Importar os módulos criados
from configuracoes import *
from overworld import Overworld


# Criar a classe do jogo
class Jogo:
    def __init__(self):
        # Configurações iniciais de "Overworld()"
        self.level_final = 2
        self.overworld = Overworld(0, self.level_final, tela)

    def executar(self):
        """Função responsável pela execução do jogo"""
        self.overworld.executar()


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
    tela.fill('black')

    # Iniciar o jogo
    jogo.executar()

    # Atualizar a tela
    pygame.display.update()

    # FPS
    relogio.tick(60)
