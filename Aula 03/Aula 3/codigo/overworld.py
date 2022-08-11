# ToDo: 23:00 minutos do vídeo
# Importar as bibliotecas
import pygame

# Importar os módulos criados
from dados_jogo import levels


class No(pygame.sprite.Sprite):
    def __init__(self, posicao, estado):
        super().__init__()
        # Criar a imagem e o rect do no
        self.image = pygame.Surface((100, 80))
        if estado == 'disponivel':
            self.image.fill('red')
        else:
            self.image.fill('gray')
        self.rect = self.image.get_rect(center=posicao)


class Overworld:
    def __init__(self, level_inicial, level_final, tela):
        # Configurações iniciais
        self.tela = tela
        self.level_final = level_final
        self.level_atual = level_inicial

        # Configurações dos sprites
        self.configuracao_nos()

    def configuracao_nos(self):
        """Função responsável por configurar os nós do mapa do overworld"""
        # Criar o grupo dos sprites para os nós
        self.nos = pygame.sprite.Group()

        # Verificar se o level do nó é menor ou igual ao "level_final" e colocar cada nó na tela
        for indice_no, dados_nos in enumerate(levels.values()):
            if indice_no <= self.level_final:
                sprite_no = No(dados_nos['pos_no'], 'disponivel')
            else:
                sprite_no = No(dados_nos['pos_no'], 'indisponivel')
            self.nos.add(sprite_no)

    def executar(self):
        """Função responsável por executar o overworld"""
        # Desenhar o Overworld na tela
        self.nos.draw(self.tela)
