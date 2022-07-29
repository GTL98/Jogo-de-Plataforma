# Importar as bibliotecas
import pygame

# Importar os módulos criados
from configuracoes import *


# Criar a classe do jogador
class Jogador(pygame.sprite.Sprite):
    # Definir as variáveis iniciais da classe
    def __init__(self, posicao):
        super().__init__()

        # Criar a imagem
        self.image = pygame.Surface((32, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=posicao)

        # Configurações do movimento do personagem
        self.velocidade = 8
        self.direcao = pygame.math.Vector2(0, 0)

    def obter_entrada(self):
        """Função destinada a obter a entrada de comandos do jogador"""
        # Criar uma lista com todas as teclas possíveis de serem pressionadas
        teclas = pygame.key.get_pressed()

        # Mover para a direita
        if teclas[pygame.K_RIGHT]:
            self.direcao.x = 1

        # Mover para a esquerda
        elif teclas[pygame.K_LEFT]:
            self.direcao.x = -1

        # O personagem fica parado
        else:
            self.direcao.x = 0

    def update(self):
        """Função destinada a atualizar o personagem"""
        # Obter a entrada do jogador
        self.obter_entrada()

        # Atualizar a posição do personagem
        self.rect.x += self.direcao.x * self.velocidade
