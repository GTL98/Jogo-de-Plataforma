# Importar as bibliotecas
import pygame

# Importar os módulos criados
from configuracoes import *
from tiles import Tile, TileEstatico
from suporte import importar_layout_csv, importar_tiles_cortados


class Level:
    def __init__(self, dados_level, tela):
        # Configurações iniciais do mapa do level
        self.tela = tela
        self.velocidade_mapa = 0

        # Configurações do terreno do mapa do level
        terreno_layout = importar_layout_csv(dados_level['terreno'])
        self.terreno_sprites = self.criar_grupo_tile(terreno_layout, 'terreno')

    def criar_grupo_tile(self, layout, tipo):
        """Função destinada a criar o grupo de sprites do tile informado"""
        # Criar o grupo onde será armazenado os sprites do tile informado
        grupo_sprite = pygame.sprite.Group()

        # Pegar a linha e o índice da linha em si
        for indice_linha, linha in enumerate(layout):
            # Pegar a posição de cada item ("celula") dentro da linha, bem como o item em si
            for indice_coluna, celula in enumerate(linha):
                # Dependendo do valor de "celula", então será colocado algo na tela nessa posição
                if celula != '-1':  # sempre passar uma string porque no arquivo CSV está como string
                    x = indice_coluna * TAMANHO_TILE
                    y = indice_linha * TAMANHO_TILE

                    # Dependendo da informação em "tipo", será adicionado ao grupo os sprites desse tipo
                    if tipo == 'terreno':
                        lista_terreno_tile = importar_tiles_cortados('../graficos/terreno/terreno_tiles.png')
                        tile_imagem = lista_terreno_tile[int(celula)]
                        sprite = TileEstatico(TAMANHO_TILE, x, y, tile_imagem)
                        grupo_sprite.add(sprite)

        return grupo_sprite

    def executar(self):
        """Função destinada a executar o mapa do level"""
        # Desenhar o terreno do mapa do level
        self.terreno_sprites.update(self.velocidade_mapa)
        self.terreno_sprites.draw(self.tela)
