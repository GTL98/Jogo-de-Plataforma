# Importar as bibliotecas
import pygame

# Importar os módulos criados
from configuracoes import *
from suporte import importar_arquivos


# Criar a classe do jogador
class Jogador(pygame.sprite.Sprite):
    # Definir as variáveis iniciais da classe
    def __init__(self, posicao):
        super().__init__()

        # Configurações da imagem
        self.importar_sprites_personagem()
        self.indice_frame = 0
        self.velocidade_animacao = 0.15
        self.image = self.animacoes['parado'][self.indice_frame]
        self.rect = self.image.get_rect(topleft=posicao)

        # Configurações do movimento do personagem
        self.velocidade = 8
        self.gravidade = 0.8
        self.velocidade_pulo = -16
        self.direcao = pygame.math.Vector2(0, 0)

        # Configurações do estado do personagem
        self.estado = 'parado'
        self.olhar_direita = True
        self.no_chao = False
        self.no_teto = False
        self.na_direita = False
        self.na_esquerda = False

    def importar_sprites_personagem(self):
        """Função destinada a importar os sprites do personagem"""
        # Informar onde estão os sprites do personagem
        caminho_imagens = '../graficos/personagem/'

        # Armazenar cada tipo de animação em um dicionário
        self.animacoes = {'parado': [], 'correr': [], 'pular': [], 'cair': []}

        # Cada valor do dicionário receberá o caminho de cada arquivo presente na pasta
        for animacao in self.animacoes.keys():
            caminho_completo = f'{caminho_imagens}{animacao}'
            self.animacoes[animacao] = importar_arquivos(caminho_completo)

    def animar(self):
        """Função destinada a animar o personagem"""
        # Obter a animação desejada
        animacao = self.animacoes[self.estado]

        # Adicionar a velocidade de animação para a troca do índice do frame
        self.indice_frame += self.velocidade_animacao
        # Sempre que o valor do índice do frame passar da quantidade de imagens no diretório,
        # esse índice voltará para 0 para que recomeçe a animação
        if self.indice_frame >= len(animacao):
            self.indice_frame = 0

        # Montar a animação
        # Deve ser um objeto "int" porque a velocidade de animação é em "float" e não tem como existir
        # 0.15 imagem, por isso o "int" é necessário para que o pygame pegue somente o valor inteiro
        imagem = animacao[int(self.indice_frame)]

        # Verificar o lado que o personagem está olhando
        if self.olhar_direita:
            self.image = imagem
        else:
            imagem_invertida = pygame.transform.flip(imagem, True, False)  # inverter no eixo X e não no Y
            self.image = imagem_invertida

        # Configurar o rect da imagem
        if self.no_chao and self.na_direita:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)  # pega o rect da imagem anterior
        elif self.no_chao and self.na_esquerda:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)  # pega o rect da imagem anterior
        elif self.no_chao:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)  # pega o rect da imagem anterior
        elif self.no_teto and self.na_direita:
            self.rect = self.image.get_rect(topright=self.rect.topright)  # pega o rect da imagem anterior
        elif self.no_teto and self.na_esquerda:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)  #pega o rect da imagem anterior
        elif self.no_teto:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)  # pega o rect da imagem anterior
        else:
            self.rect = self.image.get_rect(center=self.rect.center)  # pega o rect da imagem anterior

    def obter_entrada(self):
        """Função destinada a obter a entrada de comandos do jogador"""
        # Criar uma lista com todas as teclas possíveis de serem pressionadas
        teclas = pygame.key.get_pressed()

        # Mover para a direita
        if teclas[pygame.K_RIGHT]:
            self.direcao.x = 1
            self.olhar_direita = True

        # Mover para a esquerda
        elif teclas[pygame.K_LEFT]:
            self.direcao.x = -1
            self.olhar_direita = False

        # O personagem fica parado
        else:
            self.direcao.x = 0

        # Pular
        if teclas[pygame.K_UP] and self.no_chao:
            self.pulo()

    def obter_estado(self):
        """Função destinada a obter o estado do personagem para aplicar a animação correta"""
        # Pular
        if self.direcao.y < 0:
            self.estado = 'pular'

        # Cair
        elif self.direcao.y > 1:  # Usar um valor maior do que "self.gravidade" evita que o personagem fique flicando
            self.estado = 'cair'

        # Parado ou correr
        else:
            # Correr
            if self.direcao.x != 0:
                self.estado = 'correr'

            # Parado
            else:
                self.estado = 'parado'

    def aplicar_gravidade(self):
        """Função destinada a aplicar a gravidade no personagem"""
        # Adicionar a gravidade no eixo Y do personagem
        self.direcao.y += self.gravidade
        self.rect.y += self.direcao.y

    def pulo(self):
        """Função destinada a configurar o pular do personagem"""
        self.direcao.y = self.velocidade_pulo

    def update(self):
        """Função destinada a atualizar o personagem"""
        # Entrada do jogador
        self.obter_entrada()

        # Estado do persongem
        self.obter_estado()

        # Animação do personagem
        self.animar()
