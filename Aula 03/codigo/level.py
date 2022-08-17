# Importar as bibliotecas
import pygame

# Importar os módulos criados
from tiles import *
from decoracao import *
from configuracoes import *
from inimigo import Inimigo
from jogador import Jogador
from dados_jogo import levels
from particulas import EfeitoParticula
from suporte import importar_layout_csv, importar_tiles_cortados


class Level:
    def __init__(self, level_atual, tela, criar_overworld):
        # Configurações iniciais do mapa
        horizonte_ceu = 8
        self.tela = tela
        quantidade_nuvens = 20
        horizonte_nuvens = 400
        altura_agua = ALTURA - 30
        self.velocidade_mapa = 0

        # Conexão com o Overworld
        self.criar_overworld = criar_overworld
        self.level_atual = level_atual
        dados_level = levels[self.level_atual]
        self.novo_level_final = dados_level['desbloquear']


        # Configurações do personagem
        personagem_layout = importar_layout_csv(dados_level['personagem'])
        self.personagem = pygame.sprite.GroupSingle()
        self.fim_fase = pygame.sprite.GroupSingle()
        self.configuracoes_personagem(personagem_layout)
        self.x_atual = None

        # Configurações das partículas de poeira
        self.particula_sprites = pygame.sprite.GroupSingle()
        self.personagem_no_chao = False

        # Configurações do terreno do mapa
        terreno_layout = importar_layout_csv(dados_level['terreno'])
        self.terreno_sprites = self.criar_grupo_tile(terreno_layout, 'terreno')

        # Configurações da grama do mapa
        grama_layout = importar_layout_csv(dados_level['grama'])
        self.grama_sprites = self.criar_grupo_tile(grama_layout, 'grama')

        # Configurações das caixas do mapa
        caixas_layout = importar_layout_csv(dados_level['caixas'])
        self.caixas_sprites = self.criar_grupo_tile(caixas_layout, 'caixas')

        # Configurações das moedas do mapa
        moedas_layout = importar_layout_csv(dados_level['moedas'])
        self.moedas_sprites = self.criar_grupo_tile(moedas_layout, 'moedas')

        # Configurações das parlmeiras da frente
        palmeiras_frente_layout = importar_layout_csv(dados_level['palmeiras_frente'])
        self.palmeiras_frente_sprites = self.criar_grupo_tile(palmeiras_frente_layout, 'palmeiras_frente')

        # Configurações das palmeiras do fundo
        palmeiras_fundo_layout = importar_layout_csv(dados_level['palmeiras_fundo'])
        self.palmeiras_fundo_sprites = self.criar_grupo_tile(palmeiras_fundo_layout, 'palmeiras_fundo')

        # Configurações dos inimigos
        inimigos_layout = importar_layout_csv(dados_level['inimigos'])
        self.inimigos_sprites = self.criar_grupo_tile(inimigos_layout, 'inimigos')

        # Configurações dos limites dos inimigos
        limites_layout = importar_layout_csv(dados_level['limites'])
        self.limites_sprites = self.criar_grupo_tile(limites_layout, 'limites')

        # Configurações das decorações
        largura_level = len(terreno_layout[0]) * TAMANHO_TILE  # qualquer linha do arquivo CSV do terreno já dá a largura do level
        self.ceu = Ceu(horizonte_ceu)
        self.agua = Agua(altura_agua, largura_level)
        self.nuvens = Nuvens(horizonte_nuvens, largura_level, quantidade_nuvens)

    def criar_grupo_tile(self, layout, tipo):
        """Função responável por criar o grupo de sprites do tile informado"""
        # Criar o grupo onde será armazenado os sprites do tile informado
        grupo_sprite = pygame.sprite.Group()

        # Pegar a linha e o índice da linha em si
        for indice_linha, linha in enumerate(layout):
            # Pegar a posição de cada item ("celula") dentro da linha, bem como o item em si
            for indice_coluna, celula in enumerate(linha):
                # Dependendo do valor de "celula", então será colocado algo na tela nessa posição
                if celula != '-1':  # sempre passar uma string porque no arquivo CSV está como string
                    x = indice_coluna * TAMANHO_TILE
                    y = indice_linha * TAMANHO_TILE

                    # Dependendo da informação em "tipo", será adicionado ao grupo os sprites desse tipo
                    if tipo == 'terreno':
                        lista_terreno_tile = importar_tiles_cortados('../graficos/terreno/terreno_tiles.png')
                        tile_imagem = lista_terreno_tile[int(celula)]
                        sprite = TileEstatico(TAMANHO_TILE, x, y, tile_imagem)

                    if tipo == 'grama':
                        lista_grama_tile = importar_tiles_cortados('../graficos/decoracao/grama/grama.png')
                        tile_imagem = lista_grama_tile[int(celula)]
                        sprite = TileEstatico(TAMANHO_TILE, x, y, tile_imagem)

                    if tipo == 'caixas':
                        sprite = Caixas(TAMANHO_TILE, x, y)

                    if tipo == 'moedas':
                        if celula == '0':
                            caminho = '../graficos/moedas/ouro/'  # moedas de ouro
                        else:
                            caminho = '../graficos/moedas/prata/'  # moedas de prata

                        sprite = Moedas(TAMANHO_TILE, x, y, caminho)

                    if tipo == 'palmeiras_frente':
                        if celula == '0':
                            # Palmeiras pequenas
                            caminho = '../graficos/terreno/palmeiras_frente_pequena/'
                            deslocamento = 38
                        else:
                            # Palmeiras grandes
                            caminho = '../graficos/terreno/palmeiras_frente_grande/'
                            deslocamento = 64

                        sprite = Palmeiras(TAMANHO_TILE, x, y, caminho, deslocamento)

                    if tipo == 'palmeiras_fundo':
                        caminho = '../graficos/terreno/palmeiras_fundo/'
                        deslocamento = 64
                        sprite = Palmeiras(TAMANHO_TILE, x, y, caminho, deslocamento)

                    if tipo == 'inimigos':
                        sprite = Inimigo(TAMANHO_TILE, x, y)

                    if tipo == 'limites':
                        sprite = Tile(TAMANHO_TILE, x, y)

                    grupo_sprite.add(sprite)

        return grupo_sprite

    def configuracoes_personagem(self, layout):
        """Função responsável por criar os sprites do personagem"""
        # Pegar a linha e o índice da linha em si
        for indice_linha, linha in enumerate(layout):
            # Pegar a posição de cada item ("celula") dentro da linha, bem como o item em si
            for indice_coluna, celula in enumerate(linha):
                x = indice_coluna * TAMANHO_TILE
                y = indice_linha * TAMANHO_TILE
                # Dependendo do valor de "celula", então será colocado algo na tela nessa posição
                if celula == '0':  # personagem
                    sprite = Jogador((x, y), self.tela, self.criar_particulas_pulo)
                    self.personagem.add(sprite)
                if celula == '1':  # fim da fase
                    chapeu = pygame.image.load('../graficos/personagem/chapeu.png').convert_alpha()
                    sprite = TileEstatico(TAMANHO_TILE, x, y, chapeu)
                    self.fim_fase.add(sprite)

    def colisao_inimigo_reverso(self):
        """Função responsável por inverter o movimento do inimigo quando ele chegar perto do abismo"""
        for inimigo in self.inimigos_sprites.sprites():
            if pygame.sprite.spritecollide(inimigo, self.limites_sprites, False):
                inimigo.reverso()

    def colisao_horizontal(self):
        """Função responsável por verificar a colisão do personagem na horizontal"""
        # Obter as informações do sprite do personagem
        personagem = self.personagem.sprite
        personagem.rect.x += personagem.direcao.x * personagem.velocidade

        # Detectar a colisão entre o personagem e o chão, as caixas e as palmeiras da frente
        sprites_colidiveis = self.terreno_sprites.sprites() +\
                             self.caixas_sprites.sprites() + self.palmeiras_frente_sprites.sprites()
        for sprite in sprites_colidiveis:
            if sprite.rect.colliderect(personagem.rect):
                # O lado esquerdo do personagem encosta no lado direito do tile
                if personagem.direcao.x < 0:
                    personagem.rect.left = sprite.rect.right
                    personagem.na_esquerda = True
                    self.x_atual = personagem.rect.left  # "x_atual" recebe o valor atual do contato do personagem com o tile
                # O lado direito do personagem encosta no lado esquerdo do tile
                elif personagem.direcao.x > 0:
                    personagem.rect.right = sprite.rect.left
                    personagem.na_direita = True
                    self.x_atual = personagem.rect.right  # "x_atual" recebe o valor atual do contato do personagem com o tile

        # Informar ao código que o personagem já passou do obtáculo da esquerda ou só pode encostar e voltar
        if personagem.na_esquerda and (personagem.rect.left < self.x_atual or personagem.direcao.x >= 0):
            personagem.na_esquerda = False
        # Informar ao código que o personagem já passou do obtáculo da direita ou só pode encostar e voltar
        if personagem.na_direita and (personagem.rect.right > self.x_atual or personagem.direcao.x <= 0):
            personagem.na_direita = False

    def colisao_vertical(self):
        """Função responsável por verificar a colisão do personagem na vertical"""
        # Obter as informações do sprite do personagem
        personagem = self.personagem.sprite
        personagem.aplicar_gravidade()

        # Detectar a colisão entre o personagem e o chão, as caixas e as palmeiras da frente
        sprites_colidiveis = self.terreno_sprites.sprites() + \
                             self.caixas_sprites.sprites() + self.palmeiras_frente_sprites.sprites()
        for sprite in sprites_colidiveis:
            if sprite.rect.colliderect(personagem.rect):
                # A parte de baixo do personagem encosta na parte de cima do tile
                if personagem.direcao.y > 0:
                    personagem.rect.bottom = sprite.rect.top
                    personagem.direcao.y = 0  # Isso evita que o personagem passe do chão
                    personagem.no_chao = True
                # A parte de cima do personagem encosta na parte de baixo do tile
                elif personagem.direcao.y < 0:
                    personagem.rect.top = sprite.rect.bottom
                    personagem.direcao.y = 0  # Isso evita que o personagem fique grudado no teto
                    personagem.no_teto = True

        # Informar ao código que o personagem pulou e por isso "no_chao" deve ser "False"
        if personagem.no_chao and personagem.direcao.y < 0 or personagem.direcao.y > 1:
            personagem.no_chao = False

        # Informar ao código que o personagem encostou no teto e por isso "no_teto" deve ser "False"
        if personagem.no_teto and personagem.direcao.y > 0:
            personagem.no_teto = False

    def scroll_x(self):
        """Função responsável por mover o mapa inteiro quando o personagem chegar ao limite da tela
        no eixo X. Isso serve para que o jogador tenha acesso a outras partes do mapa"""
        # Obter os dados da direção do jogador
        personagem = self.personagem.sprite
        direcao_x = personagem.direcao.x
        personagem_x = personagem.rect.centerx

        # Deixar o limite para o scroll como um valor dependente da largura da tela
        limite_direito = int(LARGURA * 0.8)
        limite_esquerdo = int(LARGURA * 0.2)

        # Lado esquerdo da tela
        if personagem_x < limite_esquerdo and direcao_x < 0:  # Isso evita que o personagem vá para esquerda para sempre
            # O mapa se movimenta para a direita e o personagem fica parado,
            # o que dá a sensação de movimento para a esquerda
            self.velocidade_mapa = 8
            personagem.velocidade = 0

        # Lado direito da tela
        elif personagem_x > limite_direito and direcao_x > 0:  # Isso evita que o personagem vá para direita para sempre
            # O mapa se movimenta para a esquerda e o personagem fica parado,
            # o que dá a sensação de movimento para a direita
            self.velocidade_mapa = -8
            personagem.velocidade = 0

        # Quando o personagem não estiver nos limites da tela
        else:
            # O mapa fica parado e quem se move é o personagem
            self.velocidade_mapa = 0
            personagem.velocidade = 8

    def obter_personagem_no_chao(self):
        """Função responsável por verificar se o personagem está no chão"""
        # Verificar se o personagem está no chão
        if self.personagem.sprite.no_chao:
            self.personagem_no_chao = True
        else:
            self.personagem_no_chao = False

    def criar_particulas_pulo(self, posicao):
        """Função responsável por colocar as partículas de pulo quando o personagem pular"""
        # Verificar para que lado o personagem está olhando para ajeitar a partícula
        if self.personagem.sprite.olhar_direita:
            posicao -= pygame.math.Vector2(10, 5)
        else:
            posicao += pygame.math.Vector2(10, -5)
        # Criar o objeto que armazenará a animação da partícula durante o pulo
        particula_pulo_sprite = EfeitoParticula(posicao, 'pulo')

        # Adicionar à lista de sprites os sprites de "pulo"
        self.particula_sprites.add(particula_pulo_sprite)

    def criar_particulas_pouso(self):
        """Função responsável por colocar as partículas de pouso quando o personagem tocar o chão
        depois de ter pulado"""
        # Verificar para que lado o personagem está olhando para ajeitar a partícula
        if self.personagem.sprite.olhar_direita:
            posicao = self.personagem.sprite.rect.midbottom - pygame.math.Vector2(10, 15)
        else:
            posicao = self.personagem.sprite.rect.midbottom - pygame.math.Vector2(-10, 15)

        # Verificar se o personagem está no chão e já tenha pulado antes e se a lista "self.sprite_particula"
        # está vazia. Isso serve para evitar que a animação das partículas de pouso sejam criadas várias
        # vezes
        if not self.personagem_no_chao and self.personagem.sprite.no_chao and not self.particula_sprites:
            particula_pouso_sprite = EfeitoParticula(posicao, 'pouso')
            self.particula_sprites.add(particula_pouso_sprite)

    def checar_morte(self):
        """Função responsável por verificar se o personagem morreu"""
        # Verificar se o personagem caiu no abismo
        if self.personagem.sprite.rect.top > ALTURA:
            self.criar_overworld(self.level_atual, 0)  # como o personagem morreu, não pode liberar o level seguinte

    def checar_vitoria(self):
        """Função responsável por verificar se o personagem encostou no chapéu do fim do level"""
        if pygame.sprite.spritecollide(self.personagem.sprite, self.fim_fase, False):
            self.criar_overworld(self.level_atual, self.novo_level_final)  # liberar o level seguinte quando o personagem encostar no chapéu, que indica o fim do level

    def executar(self):
        """Função responsável por executar o mapa do level"""
        # Desenhar o céu do mapa
        self.ceu.desenhar(self.tela)

        # Desenhar as nuvens do mapa
        self.nuvens.desenhar(self.tela, self.velocidade_mapa)

        # Desenhar as palmeiras do fundo do mapa
        self.palmeiras_fundo_sprites.update(self.velocidade_mapa)
        self.palmeiras_fundo_sprites.draw(self.tela)

        # Desenhar o terreno do mapa
        self.terreno_sprites.update(self.velocidade_mapa)
        self.terreno_sprites.draw(self.tela)

        # Desenhar os inimigos do mapa
        self.inimigos_sprites.update(self.velocidade_mapa)
        self.inimigos_sprites.draw(self.tela)

        # Colocar os limites dos inimigos do mapa
        self.limites_sprites.update(self.velocidade_mapa)

        # Inverter o inimigo quando ele chega no abismo
        self.colisao_inimigo_reverso()

        # Desenhar as caixas do mapa
        self.caixas_sprites.update(self.velocidade_mapa)
        self.caixas_sprites.draw(self.tela)

        # Desenhar a grama do mapa
        self.grama_sprites.update(self.velocidade_mapa)
        self.grama_sprites.draw(self.tela)

        # Desenhar as moedas do mapa
        self.moedas_sprites.update(self.velocidade_mapa)
        self.moedas_sprites.draw(self.tela)

        # Desenhar as palmeiras da frente do mapa
        self.palmeiras_frente_sprites.update(self.velocidade_mapa)
        self.palmeiras_frente_sprites.draw(self.tela)

        # Desenhar as partículas no mapa
        self.particula_sprites.update(self.velocidade_mapa)
        self.particula_sprites.draw(self.tela)

        # Atualizar o personagem
        self.personagem.update()

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

        # Movimentar o mapa quando o personagem chegar ao limite da tela
        self.scroll_x()

        # Desenhar o personagem
        self.personagem.draw(self.tela)

        # Desenhar o fim da fase do mapa
        self.fim_fase.update(self.velocidade_mapa)
        self.fim_fase.draw(self.tela)

        # Verificar se o personagem morreu
        self.checar_morte()

        # Veritifcar se o personagem ganhou o level
        self.checar_vitoria()

        # Desenhar a água do mapa
        self.agua.desenhar(self.tela, self.velocidade_mapa)
