# Importar as bibliotecas
import pygame
from random import choice, randint

# Importar os módulos criados
from configuracoes import *
from suporte import importar_arquivos
from tiles import TileAnimado, TileEstatico


class Ceu:
    def __init__(self, horizonte, estilo='level'):
        # Horizonte
        self.horizonte = horizonte

        # Carregar as imagens
        self.topo = pygame.image.load('../graficos/decoracao/ceu/ceu_topo.png').convert()
        self.meio = pygame.image.load('../graficos/decoracao/ceu/ceu_meio.png').convert()
        self.base = pygame.image.load('../graficos/decoracao/ceu/ceu_base.png').convert()

        # Esticar as imagens para que fiquem na largura da tela
        self.topo = pygame.transform.scale(self.topo, (LARGURA, TAMANHO_TILE))
        self.meio = pygame.transform.scale(self.meio, (LARGURA, TAMANHO_TILE))
        self.base = pygame.transform.scale(self.base, (LARGURA, TAMANHO_TILE))

        # Determinar o estilo do céu se estiver no Overworld ou nos levels
        self.estilo = estilo
        if self.estilo == 'overworld':
            # Palmeiras
            imagens_palmeiras = importar_arquivos('../graficos/overworld/palmeiras/')
            self.palmeiras = []
            # Escolher imagens aleatórias de "imagens_palmeiras" e colocar em posições aleatórias
            # na linha do horizonte
            for imagem in [choice(imagens_palmeiras) for i in range(10)]:
                # Posição X da imagem
                x = randint(0, LARGURA)
                # Posição Y da imagem
                y = (self.horizonte * TAMANHO_TILE) + randint(50, 100)
                # Obter o rect da imagem
                rect = imagem.get_rect(midbottom=(x, y))
                # Adicionar a superfície e o rect da imagem em "self.palmeiras"
                self.palmeiras.append((imagem, rect))

            # Nuvens
            imagens_nuvens = importar_arquivos('../graficos/overworld/nuvem/')
            self.nuvens = []
            # Escolher imagens aleatórias de "imagens_nuvens" e colocar em posições aleatórias
            # na linha do horizonte
            for imagem in [choice(imagens_nuvens) for i in range(10)]:
                # Posição X da imagem
                x = randint(0, LARGURA)
                # Posição Y da imagem
                y = randint(0, (self.horizonte * TAMANHO_TILE) - 100)
                # Obter o rect da imagem
                rect = imagem.get_rect(midbottom=(x, y))
                # Adicionar a superfície e o rect da imagem em "self.palmeiras"
                self.nuvens.append((imagem, rect))

    def desenhar(self, tela):
        """Função destinada a desenhar o céu no fundo da tela"""
        # Colocar o céu no fundo da tela
        for linha in range(quantidade_tile_vertical):
            y = linha * TAMANHO_TILE
            # Colocar o topo do céu somente se o valor de "linha" for menor do que "self.horizonte"
            if linha < self.horizonte:
                tela.blit(self.topo, (0, y))
            # Colocar o meio do céu somente se o valor de "linha" for igual ao "self.horizonte"
            elif linha == self.horizonte:
                tela.blit(self.meio, (0, y))
            # Colocar a base do céu somente se o valor de "linha" for maior do que "self.horizonte"
            else:
                tela.blit(self.base, (0, y))

        # Desenhar as palmeiras e as nuvens no Overworld
        if self.estilo == 'overworld':
            for palmeira in self.palmeiras:
                tela.blit(palmeira[0], palmeira[1])
            for nuvem in self.nuvens:
                tela.blit(nuvem[0], nuvem[1])


class Agua:
    def __init__(self, topo, largura_level):
        # Configurações iniciais
        caminho = '../graficos/decoracao/agua/'
        comeco_agua = -LARGURA  # terá água mais para a esquerda do mapa
        largura_agua = 192  # largura do sprite da água (ver as dimensões das imagens)
        quantidade_agua_tile = int((largura_level + LARGURA) / largura_agua)

        # Criar o grupo de sprites para armazenar os sprites da água
        self.agua_sprites = pygame.sprite.Group()

        # Colocar os tiles da água ao longo do mapa, respeitando o valor máximo de tiles em "quantidade_agua_tile"
        for tile in range(quantidade_agua_tile):
            x = (tile * largura_agua + comeco_agua) + 500  # adicionar 500 para que a água não termine tão perto de "largura_agua")
            y = topo
            sprite = TileAnimado(largura_agua, x, y, caminho)
            self.agua_sprites.add(sprite)

    def desenhar(self, tela, velocidade_mundo):
        """Função destinada a desenhar a água no mapa"""
        self.agua_sprites.update(velocidade_mundo)
        self.agua_sprites.draw(tela)


class Nuvens:
    def __init__(self, horizonte, largura_level, quantidade_nuvens):
        # Adicionar a uma lista as imagens das nuvens
        lista_nuvens = importar_arquivos('../graficos/decoracao/nuvem/')

        # Configuração das posições das nuvens
        x_min = -LARGURA
        x_max = largura_level + LARGURA
        y_min = 0
        y_max = horizonte

        # Criar o grupo de sprites para armazenar os sprites das nuvens
        self.nuvens_sprites = pygame.sprite.Group()

        # Escolher aleatoriamente uma imagem de "lista_nuvens"
        for i in range(quantidade_nuvens):
            nuvem = choice(lista_nuvens)
            # Posição X e Y das nuvens na tela
            x = randint(x_min, x_max)
            y = randint(y_min, y_max)
            sprite = TileEstatico(0, x, y, nuvem)
            self.nuvens_sprites.add(sprite)

    def desenhar(self, tela, velocidade_mapa):
        """Função destinada a desenhar as nuvens no céu do mapa"""
        self.nuvens_sprites.update(velocidade_mapa)
        self.nuvens_sprites.draw(tela)