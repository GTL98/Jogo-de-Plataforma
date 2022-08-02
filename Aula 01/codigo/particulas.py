# Importar as bibliotecas
import pygame

# Importar os módulo criados
from suporte import importar_arquivos


class EfeitoParticula(pygame.sprite.Sprite):
    def __init__(self, posicao, tipo_animacao):
        super().__init__()
        # Configurações da animação
        self.indice_frame = 0
        self.velocidade_animacao = 0.5

        # Importar o sprites de pulo quando o personagem pular
        if tipo_animacao == 'pulo':
            self.frames = importar_arquivos('../graficos/personagem/particulas_poeira/pulo')
        if tipo_animacao == 'pouso':
            self.frames = importar_arquivos('../graficos/personagem/particulas_poeira/pouso')

        # Configurações das imagens
        self.image = self.frames[self.indice_frame]
        self.rect = self.image.get_rect(center=posicao)

    def animar(self):
        """Função destinada a animar as partículas"""
        # Se "self.indice_frame" for maior ou igual ao tamanho de "self.frames"
        # o efeito da partícula deve ser retirado da tela, para isso é usado o método "kill()"
        self.indice_frame += self.velocidade_animacao
        if self.indice_frame >= len(self.frames):
            self.kill()
        # Se "self.indice_frame" não for maior que o tamanho de "self.frames", isso indica que
        # a animação ainda deve continuar
        else:
            self.image = self.frames[int(self.indice_frame)]

    def update(self, velocidade_mapa):
        """Função destinada a atualizar as partículas"""
        # Animação das partículas
        self.animar()

        # As partículas de pulo e pouso devem ficar estáticas em relação ao personagem
        self.rect.x += velocidade_mapa
