# Importar as bibliotecas
import pygame
from random import randint

# Importar os módulos criados
from tiles import TileAnimado


class Inimigo(TileAnimado):
    def __init__(self, tamanho, x, y):
        # Caminho do diretório dos sprites dos inimigos
        caminho = '../graficos/inimigo/correr/'
        super().__init__(tamanho, x, y, caminho)

        # Ajustar os sprites dos inimigos
        tamanho_imagem = tamanho - self.image.get_size()[1]
        self.rect.y += tamanho_imagem

        # Velocidade randômica
        self.velocidade = randint(3, 5)

    def movimento(self):
        """Função destinada a realizar o movimento do personagem"""
        # Movimentar horizontalmente o inimigo
        self.rect.x += self.velocidade

    def inverter_sprite(self):
        """Função destinada a inverter o sprite quando o inimigo estiver indo para um lado
        Inverter à direita quando o inimigo estiver indo à direita
        Inverter à esquerda quando o inimigo estiver indo à esquerda"""
        # Se o inimigo estiver indo para a direita, virar os sprites para a direita
        if self.velocidade > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverso(self):
        """Função destinada a inverter a velocidade quando o inimigo chega perto do abismo"""
        # Inverter a velocidade
        self.velocidade *= -1

    def update(self, velocidade_mapa):
        """Função destinada a atualizar os inimigos no mapa"""
        # Movimentar o mundo quando o personagem chegar aos limites do mapa
        self.rect.x += velocidade_mapa

        # Animar os inimigos
        self.animar()

        # Movimentar os inimigos
        self.movimento()

        # Inverter os sprites
        self.inverter_sprite()
