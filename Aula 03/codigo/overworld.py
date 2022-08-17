# Importar as bibliotecas
import pygame

# Importar os módulos criados
from decoracao import Ceu
from dados_jogo import levels
from suporte import importar_arquivos


class No(pygame.sprite.Sprite):
    def __init__(self, posicao, estado, velocidade_icone, caminho):
        super().__init__()
        # Criar a imagem e o rect do nó
        self.frames = importar_arquivos(caminho)
        self.indice_frame = 0
        self.velocidade_animacao = 0.15
        self.image = self.frames[self.indice_frame]
        if estado == 'disponivel':
            self.estado = 'disponivel'
        else:
            self.estado = 'indisponivel'
        self.rect = self.image.get_rect(center=posicao)

        # Configurações da zona de detecção de colisão
        esquerda = self.rect.centerx - (velocidade_icone / 2)
        topo = self.rect.centery - (velocidade_icone / 2)
        self.zona_deteccao = pygame.Rect(esquerda, topo, velocidade_icone, velocidade_icone)

    def animar(self):
        """Função responsável por animar os nós no Overworld"""
        self.indice_frame += self.velocidade_animacao
        if self.indice_frame >= len(self.frames):
            self.indice_frame = 0
        self.image = self.frames[int(self.indice_frame)]

    def update(self):
        """Função responsável por atualizar os nós no Overworld"""
        # Animar os nós somente quando o level estiver disponível
        if self.estado == 'disponivel':
            self.animar()
        # Deixar apagado os nós que estão indisponíveis
        else:
            # Copiar a imagem
            no_indisponivel = self.image.copy()

            # Preencher a imagem
            # 1: Cor
            # 2: Objeto Rect
            # 3: Flags (essa flag usada serve para pintar somente os pixels que está o sprite,
            #           onde não tiver sprite, ou seja, o valor de Alfa como 0, não é pintado)
            no_indisponivel.fill('black', None, pygame.BLEND_RGBA_MULT)

            # Colocar a máscara nos nós indisponíveis
            self.image.blit(no_indisponivel, (0, 0))


class Icone(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        # Criar a imagem e o rect do ícone no Overworld
        self.posicao = posicao  # isso permite usar valores "float" para movimentar o ícone
        self.image = pygame.image.load('../graficos/overworld/chapeu.png').convert_alpha()
        self.rect = self.image.get_rect(center=posicao)

    def update(self):
        """Função responsável por atualizar o sprite do ícone no Overworld"""
        self.rect.center = self.posicao


class Overworld:
    def __init__(self, level_inicial, level_final, tela, criar_level):
        # Configurações iniciais
        self.tela = tela
        self.level_final = level_final
        self.level_atual = level_inicial
        self.criar_level = criar_level
        horizonte = 8

        # Configurações da lógica do movimento no Overworld
        self.movendo = False
        self.velocidade = 8
        self.mover_direcao = pygame.math.Vector2(0, 0)

        # Configurações dos sprites
        self.configuracao_nos()
        self.configuracao_icone()
        self.ceu = Ceu(horizonte, 'overworld')

    def configuracao_nos(self):
        """Função responsável por configurar os nós do mapa do Overworld"""
        # Criar o grupo dos sprites para os nós
        self.nos = pygame.sprite.Group()

        # Verificar se o level do nó é menor ou igual ao "level_final" e colocar cada nó na tela
        for indice_no, dados_nos in enumerate(levels.values()):
            if indice_no <= self.level_final:
                sprite_no = No(dados_nos['pos_no'],
                               'disponivel',
                               self.velocidade,
                               dados_nos['graficos_no'])
            else:
                sprite_no = No(dados_nos['pos_no'],
                               'indisponivel',
                               self.velocidade,
                               dados_nos['graficos_no'])

            # Adicionar os sprites dos nós ao grupo
            self.nos.add(sprite_no)

    def configuracao_icone(self):
        """Função responsável por configurar o ícone do mapa do Overworld"""
        # Criar o grupo de sprite para o ícone
        self.icone = pygame.sprite.GroupSingle()

        # Criar um sprite para o ícone
        # Usar os sprites dos nós, uma vez que já possuímos a posição XY e em qual "self.level_atual"
        # essa posição está na tela
        sprite_icone = Icone(self.nos.sprites()[self.level_atual].rect.center)

        # Adicionar o sprite do ícone ao grupo
        self.icone.add(sprite_icone)

    def desenhar_linhas(self):
        """Função responsável por desenhar as linhas entre os nós"""
        # Desenhar as linhas entre os levels no Overworld depois que o jogador passar do primeiro level
        if self.level_final > 0:
            # Criar uma lista com as posições dos nós para desenhar as linhas
            pontos = [no['pos_no'] for indice_no,
                      no in enumerate(levels.values()) if indice_no <= self.level_final]

            # Desenhar as linhas entre os nós
            # 1: Onde desenhar
            # 2: Cor
            # 3: Preenchimento
            # 4: Ponto de partida e de chegada
            # 5: Espessura da linha
            pygame.draw.lines(self.tela, '#a04f45', False, pontos, 6)

    def entrada(self):
        """Função responsável por obter a entrada de teclas do jogador"""
        # Criar uma lista com as teclas
        teclas = pygame.key.get_pressed()

        # O ícone só se moverá depois de um certo tempo
        if not self.movendo:
            # Verificar se as teclas foram pressionadas
            if teclas[pygame.K_RIGHT] and self.level_atual < self.level_final:
                # Mover o ícone pelo Overworld
                self.mover_direcao = self.obter_dados_movimento('seguinte')
                # Ir para frente até o valor de "self.level_final"
                self.level_atual += 1
                self.movendo = True

            elif teclas[pygame.K_LEFT] and self.level_atual > 0:
                # Mover o ícone pelo Overworld
                self.mover_direcao = self.obter_dados_movimento('anterior')
                # Ir para trás somente quando o ícone não estiver em "self.level_atual" igual a 0
                self.level_atual -= 1
                self.movendo = True

            elif teclas[pygame.K_SPACE]:
                # Entrar no level em que o ícone estiver
                self.criar_level(self.level_atual)

    def obter_dados_movimento(self, sentido):
        """Função responsável a obter os dados dos movimentos do ícone no Overworld"""
        # Obter a posição de saída
        comeco = pygame.math.Vector2(self.nos.sprites()[self.level_atual].rect.center)

        # Posição de cheganda a frente
        if sentido == 'seguinte':
            # Obter a posição de chegada
            final = pygame.math.Vector2(self.nos.sprites()[self.level_atual + 1].rect.center)

        # Posição de chegada atrás
        elif sentido == 'anterior':
            # Obter a posição de chegada
            final = pygame.math.Vector2(self.nos.sprites()[self.level_atual - 1].rect.center)

        # Obter o delta
        delta = final - comeco

        # Normalizar os valores para que fiquem dentro dos limites da tela
        return delta.normalize()

    def movimentar_icone(self):
        """Função responsável a movimentar o ícone no Overworld"""
        # Movimentar o ícone somente quando for permitido e quando estiver no centro do nó
        if self.movendo and self.mover_direcao:
            # Colocar o ícone no centro do nó de "self.level_atual"
            self.icone.sprite.posicao += self.mover_direcao * self.velocidade
            no_alvo = self.nos.sprites()[self.level_atual]

            # Detectar a colisão do sprite do ícone com o Rect inscrito no nó
            if no_alvo.zona_deteccao.collidepoint(self.icone.sprite.posicao):
                self.movendo = False
                self.mover_direcao = pygame.math.Vector2(0, 0)

    def executar(self):
        """Função responsável por executar o Overworld"""
        # Entrada de teclas do jogador
        self.entrada()

        # Movimentar o ícone no Overworld
        self.movimentar_icone()

        # Atualizar o ícone no Overworld
        self.icone.update()

        # Animar os nós no Overworld
        self.nos.update()

        # Desenhar o céu ao fundo do Overworld
        self.ceu.desenhar(self.tela)

        # Desenhar as linhas que ligam os nós
        self.desenhar_linhas()

        # Desenhar o Overworld na tela
        self.nos.draw(self.tela)

        # Desenhar o ícone em cima do nó
        self.icone.draw(self.tela)
