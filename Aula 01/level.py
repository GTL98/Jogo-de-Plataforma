# Importar as bibliotecas
import pygame

# Importar os módulos criados
from jogador import *
from tiles import Tile
from configuracoes import TAMANHO_TILE


# Criar a classe da geração do level
class Level:
    # Definir as variáveis inicias da classe
    def __init__(self, dados_level, tela):

        # Configurações inicias
        self.tela = tela
        self.configuracao_level(dados_level)

        # Configuração da velocidade do mapa
        self.velocidade_mapa = 0

    def configuracao_level(self, mapa):
        """Função destinada a desenhar o mapa do level"""
        # Criar o grupo de sprites para armazenar o tile
        self.tiles = pygame.sprite.Group()  # Para mais de 1 sprite da mesma classe

        # Criar o grupo de sprites para armazenar o jogador
        self.jogador = pygame.sprite.GroupSingle()  # Para somente 1 sprite de uma classe

        # Pegar o índice da linha e a linha em si
        for indice_linha, linha in enumerate(mapa):
            # Pegar a posição de cada item ("celula") dentro da linha, bem como o item em si
            for indice_coluna, celula in enumerate(linha):
                # Dependendo do valor de "celula", então será colocado algo na tela nessa posição
                x = indice_coluna * TAMANHO_TILE
                y = indice_linha * TAMANHO_TILE
                if celula == 'X':  # Desenhar o mapa
                    tile = Tile((x, y), TAMANHO_TILE)
                    self.tiles.add(tile)
                if celula == 'P':
                    jogador = Jogador((x, y))
                    self.jogador.add(jogador)

    def scroll_x(self):
        """Função destinada a mover o mapa inteiro quando o personagem chegar ao limite da tela
        no eixo X. Isso serve para que o jogador tenha acesso a outras partes do mapa"""
        # Obter os dados da direção do jogador
        jogador = self.jogador.sprite
        direcao_x = jogador.direcao.x
        jogador_x = jogador.rect.centerx

        # Deixar o limite para o scroll como um valor dependente da largura da tela
        limite_direito = int(LARGURA * 0.8)
        limite_esquerdo = int(LARGURA * 0.2)

        # Lado esquerdo da tela
        if jogador_x < limite_esquerdo and direcao_x < 0:  # Isso evita que o personagem vá para esquerda para sempre
            # O mapa se movimenta para a direita e o personagem fica parado,
            # o que dá a sensação de movimento para a esquerda
            self.velocidade_mapa = 8
            jogador.velocidade = 0

        # Lado direito da tela
        elif jogador_x > limite_direito and direcao_x > 0:  # Isso evita que o personagem vá para direita para sempre
            # O mapa se movimenta para a esquerda e o personagem fica parado,
            # o que dá a sensação de movimento para a direita
            self.velocidade_mapa = -8
            jogador.velocidade = 0

        # Quando o personagem não estiver nos limites da tela
        else:
            # O mapa fica parado e quem se move é o personagem
            self.velocidade_mapa = 0
            jogador.velocidade = 8

    def executar(self):
        """Função destinada a executar o level"""
        # Atualizar o mapa
        self.tiles.update(self.velocidade_mapa)

        # Desenhar o mapa na tela
        self.tiles.draw(self.tela)

        # Atualizar o personagem
        self.jogador.update()

        # Desenhar o personagem na tela
        self.jogador.draw(self.tela)

        # Movimentar o mapa quando o personagem chegar ao limite da tela
        self.scroll_x()
