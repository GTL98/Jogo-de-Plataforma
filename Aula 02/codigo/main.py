# Importar as bibliotecas
import sys
import pygame

# Importar os módulos criados
from level import Level
from configuracoes import *
from dados_jogo import level_0

# Configurações iniciais do Pygame
pygame.init()  # iniciar o Pygame
relogio = pygame.time.Clock()  # usar como o FPS
tela = pygame.display.set_mode((LARGURA, ALTURA))  # criar a tela
level = Level(level_0, tela)  # Criar o objeto que gerará o mapa do level

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

    # Executar o mapa do level
    level.executar()

    # Atualizar a tela
    pygame.display.update()

    # FPS
    relogio.tick(60)
