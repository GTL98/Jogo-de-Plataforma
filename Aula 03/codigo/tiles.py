# Importar as bibliotecas
import pygame

# Importar os módulos criados
from suporte import importar_arquivos


class Tile(pygame.sprite.Sprite):
    def __init__(self, tamanho, x, y):
        super().__init__()

        # Configurações do sprite
        self.image = pygame.Surface((tamanho, tamanho))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, velocidade_mapa):
        """Função responsável por atualizar o mapa quando o personagem andar"""
        # Mexer o mapa quando o personagem chegar aos limites da tela
        self.rect.x += velocidade_mapa


class TileEstatico(Tile):
    def __init__(self, tamanho, x, y, imagem):
        super().__init__(tamanho, x, y)
        # Desenhar os sprites estáticos do mapa
        self.image = imagem


class TileAnimado(Tile):
    def __init__(self, tamanho, x, y, caminho):
        super().__init__(tamanho, x, y)
        # Configurações da animação
        self.frames = importar_arquivos(caminho)
        self.indice_frame = 0
        self.image = self.frames[self.indice_frame]
        self.velocidade_frame = 0.15

    def animar(self):
        """Função responsável por animar os tiles que são programados para ser animados"""
        self.indice_frame += self.velocidade_frame
        if self.indice_frame >= len(self.frames):
            self.indice_frame = 0
        self.image = self.frames[int(self.indice_frame)]

    def update(self, velocidade_mapa):
        """Função responsável por atualizar os tiles animados"""
        # Animação
        self.animar()

        # Mexer o mapa quando o personagem chegar aos limites da tela
        self.rect.x += velocidade_mapa


class Caixas(TileEstatico):
    def __init__(self, tamanho, x, y):
        # Indicar qual é a imagem da caixa
        imagem = pygame.image.load('../graficos/terreno/caixa.png').convert_alpha()
        super().__init__(tamanho, x, y, imagem)
        # Como a imagem é menor do que o tamanho dos tiles, é necessário ajustar a posição
        # das caixas ao longo do mapa
        deslocamento_y = y + tamanho

        # Desenhar as caixas no mapa
        self.image = imagem
        self.rect = self.image.get_rect(bottomleft=(x, deslocamento_y))


class Moedas(TileAnimado):
    def __init__(self, tamanho, x, y, caminho):
        super().__init__(tamanho, x, y, caminho)
        # Valores do meio da imagem
        centro_x = x + (tamanho // 2)
        centro_y = y + (tamanho // 2)

        # Colocar as moedas no centro da imagem
        self.rect = self.image.get_rect(center=(centro_x, centro_y))


class Palmeiras(TileAnimado):
    def __init__(self, tamanho, x, y, caminho, deslocamento):
        super().__init__(tamanho, x, y, caminho)
        # Deslocamento dos sprites das palmeiras para que a base do
        # tronco fique na altura onde foi desenhada para estar
        deslocamento_y = y - deslocamento
        self.rect.topleft = (x, deslocamento_y)
