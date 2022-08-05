# Importar as bibliotecas
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, tamanho, x, y):
        super().__init__()

        # Configurações do sprite
        self.image = pygame.Surface((tamanho, tamanho))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, velocidade_mapa):
        """Função destinada a atualizar o mapa quando o personagem andar"""
        self.rect.x += velocidade_mapa


class TileEstatico(Tile):
    def __init__(self, tamanho, x, y, imagem):
        super().__init__(tamanho, x, y)
        # Desenhar os sprites estáticos do mapa
        self.image = imagem
