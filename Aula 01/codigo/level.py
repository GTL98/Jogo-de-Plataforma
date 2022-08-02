# Importar as bibliotecas
import pygame

# Importar os módulos criados
from jogador import *
from tiles import Tile
from particulas import EfeitoParticula
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

        # Configurações dos sprites das partículas
        self.sprite_paricula = pygame.sprite.GroupSingle()  # "GroupSingle()" porque é impossível pular e pousar ao mesmo tempo
        self.jogador_no_chao = False

    def criar_particulas_pulo(self, posicao):
        """Função destinada a colocar as partículas de pulo quando o personagem pular"""
        # Verificar para que lado o personagem está olhando para ajeitar a partícula
        if self.jogador.sprite.olhar_direita:
            posicao -= pygame.math.Vector2(10, 5)
        else:
            posicao += pygame.math.Vector2(10, -5)
        # Criar o objeto que armazenará a animação da partícula durante o pulo
        particula_pulo_sprite = EfeitoParticula(posicao, 'pulo')

        # Adicionar à lista de sprites os sprites de "pulo"
        self.sprite_paricula.add(particula_pulo_sprite)

    def obter_personagem_no_chao(self):
        """Função destinada a verificar se o personagem está no chão"""
        # Verificar se o personagem está no chão
        if self.jogador.sprite.no_chao:
            self.jogador_no_chao = True
        else:
            self.jogador_no_chao = False

    def criar_particulas_pouso(self):
        """Função destinada a colocar as partículas de pouso quando o personagem tocar o chão
        depois de ter pulado"""
        # Verificar para que lado o personagem está olhando para ajeitar a partícula
        if self.jogador.sprite.olhar_direita:
            posicao = self.jogador.sprite.rect.midbottom - pygame.math.Vector2(10, 15)
        else:
            posicao = self.jogador.sprite.rect.midbottom - pygame.math.Vector2(-10, 15)

        # Verificar se o personagem está no chão e já tenha pulado antes e se a lista "self.sprite_particula"
        # está vazia. Isso serve para evitar que a animação das partículas de pouso sejam criadas várias
        # vezes
        if not self.jogador_no_chao and self.jogador.sprite.no_chao and not self.sprite_paricula:
            particula_pouso_sprite = EfeitoParticula(posicao, 'pouso')
            self.sprite_paricula.add(particula_pouso_sprite)

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
                    jogador = Jogador((x, y), self.tela, self.criar_particulas_pulo)
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
        # Desenhar as partículas de pulo na tela
        self.sprite_paricula.update(self.velocidade_mapa)
        self.sprite_paricula.draw(self.tela)

        # Desenhar o mapa na tela
        self.tiles.update(self.velocidade_mapa)
        self.tiles.draw(self.tela)

        # Desenhar o personagem na tela
        self.jogador.update()
        self.jogador.draw(self.tela)

        # Movimentar o mapa quando o personagem chegar ao limite da tela
        self.scroll_x()

        # Colisão horizontal do personagem
        self.colisao_horizontal()

        # Verificar se o personagem está no chão
        # Fazer isso antes de verificar se o personagem está colidindo verticalmente para que as partículas
        # de pouso sejam criadas
        self.obter_personagem_no_chao()

        # Colisão vertical do personagem
        self.colisao_vertical()

        # Desenhar as partículas de pouso na tela
        # Deve ser feita depois da verificação de colisão vertical para que sejam criadas as partículas
        # de pouso
        self.criar_particulas_pouso()
