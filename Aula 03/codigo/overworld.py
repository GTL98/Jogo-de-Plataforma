# Importar as bibliotecas
import pygame

# Importar os módulos criados
from dados_jogo import levels


class No(pygame.sprite.Sprite):
    def __init__(self, posicao, estado):
        super().__init__()
        # Criar a imagem e o rect do nó
        self.image = pygame.Surface((100, 80))
        if estado == 'disponivel':
            self.image.fill('red')
        else:
            self.image.fill('gray')
        self.rect = self.image.get_rect(center=posicao)


class Icone(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        # Criar a imagem e o rect do ícone no Overworld
        self.image = pygame.Surface((20, 20))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=posicao)


class Overworld:
    def __init__(self, level_inicial, level_final, tela):
        # Configurações iniciais
        self.tela = tela
        self.level_final = level_final
        self.level_atual = level_inicial

        # Configurações dos sprites
        self.configuracao_nos()
        self.configuracao_icone()

    def configuracao_nos(self):
        """Função responsável por configurar os nós do mapa do Overworld"""
        # Criar o grupo dos sprites para os nós
        self.nos = pygame.sprite.Group()

        # Verificar se o level do nó é menor ou igual ao "level_final" e colocar cada nó na tela
        for indice_no, dados_nos in enumerate(levels.values()):
            if indice_no <= self.level_final:
                sprite_no = No(dados_nos['pos_no'], 'disponivel')
            else:
                sprite_no = No(dados_nos['pos_no'], 'indisponivel')

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
        # Criar uma lista com as posições dos nós para desenhar as linhas
        pontos = [no['pos_no'] for indice_no, no in enumerate(levels.values()) if indice_no <= self.level_final]

        # Desenhar as linhas entre os nós
        # 1: Onde desenhar
        # 2: Cor
        # 3: Preenchimento
        # 4: Ponto de partida e de chegada
        # 5: Espessura da linha
        pygame.draw.lines(self.tela, 'red', False, pontos, 6)

    def executar(self):
        """Função responsável por executar o Overworld"""
        # Desenhar as linhas que ligam os nós
        self.desenhar_linhas()

        # Desenhar o Overworld na tela
        self.nos.draw(self.tela)

        # Desenhar o ícone em cima do nó
        self.icone.draw(self.tela)
