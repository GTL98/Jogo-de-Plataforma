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
        self.x_atual = 0

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

    def colisao_horizontal(self):
        """Função destinada a verificar a colisão do personagem na horizontal"""
        # Obter as informações do sprite do personagem
        jogador = self.jogador.sprite
        jogador.rect.x += jogador.direcao.x * jogador.velocidade

        # Detectar a colisão entre o personagem e os tiles
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(jogador.rect):
                # O lado esquerdo do personagem encosta no lado direito do tile
                if jogador.direcao.x < 0:
                    jogador.rect.left = sprite.rect.right
                    jogador.na_esquerda = True
                    self.x_atual = jogador.rect.left  # "x_atual" recebe o valor atual do contato do personagem com o tile
                # O lado direito do personagem encosta no lado esquerdo do tile
                elif jogador.direcao.x > 0:
                    jogador.rect.right = sprite.rect.left
                    jogador.na_direita = True
                    self.x_atual = jogador.rect.right  # "x_atual" recebe o valor atual do contato do personagem com o tile

        # Informar ao código que o personagem já passou do obtáculo da esquerda ou só pode encostar e voltar
        if jogador.na_esquerda and (jogador.rect.left < self.x_atual or jogador.direcao.x >= 0):
            jogador.na_esquerda = False
        # Informar ao código que o personagem já passou do obtáculo da direita ou só pode encostar e voltar
        if jogador.na_direita and (jogador.rect.right > self.x_atual or jogador.direcao.x <= 0):
            jogador.na_direita = False

    def colisao_vertical(self):
        """Função destinada a verificar a colisão do personagem na vertical"""
        # Obter as informações do sprite do personagem
        jogador = self.jogador.sprite
        jogador.aplicar_gravidade()

        # Detectar a colisão entre o personagem e os tiles
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(jogador.rect):
                # A parte de baixo do personagem encosta na parte de cima do tile
                if jogador.direcao.y > 0:
                    jogador.rect.bottom = sprite.rect.top
                    jogador.direcao.y = 0  # Isso evita que o personagem passe do chão
                    jogador.no_chao = True
                # A parte de cima do personagem encosta na parte de baixo do tile
                elif jogador.direcao.y < 0:
                    jogador.rect.top = sprite.rect.bottom
                    jogador.direcao.y = 0  # Isso evita que o personagem fique grudado no teto
                    jogador.no_teto = True

        # Informar ao código que o personagem pulou e por isso "no_chao" deve ser "False"
        if jogador.no_chao and jogador.direcao.y < 0 or jogador.direcao.y > 1:
            jogador.no_chao = False

        # Informar ao código que o personagem encostou no teto e por isso "no_teto" deve ser "False"
        if jogador.no_teto and jogador.direcao.y > 0:
            jogador.no_teto = False

    def executar(self):
        """Função destinada a executar o level"""
        # Atualizar o mapa
        self.tiles.update(self.velocidade_mapa)

        # Desenhar o mapa na tela
        self.tiles.draw(self.tela)

        # Atualizar o personagem
        self.jogador.update()

        # Movimentar o mapa quando o personagem chegar ao limite da tela
        self.scroll_x()

        # Colisão horizontal do personagem
        self.colisao_horizontal()

        # Colisão vertical do personagem
        self.colisao_vertical()

        # Desenhar o personagem na tela
        self.jogador.draw(self.tela)
