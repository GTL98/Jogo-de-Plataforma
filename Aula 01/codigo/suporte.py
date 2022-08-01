# Importar as bibliotecas
import pygame
from os import walk


def importar_arquivos(caminho):
    """Função destinada a importar os arquivos de um determinado diretório"""
    # Criar uma lista para armazenar as imagens
    lista_imagens = []

    # A função "walk()" retorna uma tupla com 3 itens:
    # 1. O caminho do diretório
    # 2. Os subdiretórios
    # 3. Os arquivos do diretório
    for _, __, arquivos_imagens in walk(caminho):
        # "arquivos_imagens" retorna uma lista de strings com o nome de cada arquivo no diretório
        for imagem in arquivos_imagens:
            # Obter o caminho completo da imagem
            caminho_completo = f'{caminho}/{imagem}'

            # Criar a superfície da imagem
            superficie_imagem = pygame.image.load(caminho_completo).convert_alpha()

            # Adicionar a "superficie_imagem" em "lista_imagens"
            lista_imagens.append(superficie_imagem)

    return lista_imagens
