# ToDo: 42:07 minutos do vídeo!!!
# Importar as bibliotecas
import sys
import pygame

# Importar os módulos criados
from level import Level
from configuracoes import *

# Configurações inciais do Pygame
pygame.init()  # Iniciar o Pygame
relogio = pygame.time.Clock()  # Usar como o FPS
tela = pygame.display.set_mode((LARGURA, ALTURA))  # Criar a tela
level = Level(level_mapa, tela)  # Criar o objeto que gerará o level

# Game Loop
while True:
    # Eventos de interação com o Pygame
    for evento in pygame.event.get():
        # Fechar a tela quando apertar no "X"
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Preencher a tela
    tela.fill('black')

    # Executar o level
    level.executar()

    # Atualizar a janela
    pygame.display.update()  # O "update()" também consegue atualizar somente uma área da tela

    # FPS
    relogio.tick(60)
