# Importar a biblioteca
import pygame


# Criar a classe para o tiles
class Tile(pygame.sprite.Sprite):
    # Definir as variáveis iniciais da classe
    def __init__(self, posicao, tamanho):
        # Herdar as funções da classe pai
        super().__init__()

        # Criar a imagem
        self.image = pygame.Surface((tamanho, tamanho))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=posicao)

    def update(self, velocidade_x):
        """Função destinada a atualizar o mapa do level"""
        # O objeto rect movimenta no eixo X em uma determinada velocidade quando solicitado
        self.rect.x += velocidade_x
