# Importar as bibliotecas
import pygame
from os import walk
from csv import reader

# Importar os módulos criados
from configuracoes import TAMANHO_TILE


def importar_layout_csv(caminho):
    """Função destinada a importar os arquivos CSV de layout do mapa do level"""
    # Criar uma lista para armazenar cada linha do arquivo CSV
    lista_linhas = []

    # Abrir o arquivo CSV
    with open(caminho, 'r') as mapa:
        level = reader(mapa, delimiter=',')
        for linha in level:
            # Converter cada linha em uma lista para ficar mais fácil de trabalhar
            # (o "reader()" pode bugar de vez em quando)
            lista_linhas.append(list(linha))
        return lista_linhas


def importar_tiles_cortados(caminho):
    """Função destinada a importar os gráficos"""
    # Carregar a imagem
    imagem = pygame.image.load(caminho).convert_alpha()

    # Verificar quantos tiles é possível formar com as dimesões da imagem
    num_tiles_x = int(imagem.get_size()[0] / TAMANHO_TILE)
    num_tiles_y = int(imagem.get_size()[1] / TAMANHO_TILE)

    # Criar uma lista com os tiles gerados
    tiles_cortados = []

    # Saber em quantos tiles "imagem" pode ser dividida
    for linha in range(num_tiles_y):
        for coluna in range(num_tiles_x):
            # Saber a posição de cada tile em "imagem"
            x = coluna * TAMANHO_TILE
            y = linha * TAMANHO_TILE
            # Cada tile da imagem será criado separadamente, mas na mesma imagem
            # "pygame.SCRALPHA" em "flags" tira o fundo preto das imagens .png, ou seja,
            # as imagens ficam com o valor alfa do fundo como 0
            nova_imagem = pygame.Surface((TAMANHO_TILE, TAMANHO_TILE), flags=pygame.SRCALPHA)
            nova_imagem.blit(imagem, (0, 0), pygame.Rect(x, y, TAMANHO_TILE, TAMANHO_TILE))
            tiles_cortados.append(nova_imagem)

    return tiles_cortados


def importar_arquivos(caminho):
    """Função destinada a importar os arquivos para os tiles animados"""
    # Criar uma lista para armazenar imagens
    lista_imagens = []

    # Obter a imagem de cada frame da pasta que será usada para o tile animado
    for _, __, arquivos in walk(caminho):
        for arquivo in arquivos:
            caminho_completo = caminho + arquivo  # obter o caminho completo de cada imagem
            imagem = pygame.image.load(caminho_completo).convert_alpha()
            lista_imagens.append(imagem)

    return lista_imagens
