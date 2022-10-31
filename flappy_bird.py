import pygame
import os
import random

pygame.init()

#Constantes
LARGURA = 500
ALTURA = 700

#Dimensões do Chão (Base)
LARGURA_CHAO = 672       #Largura da base
ALTURA_CHAO = 112        #Altura da base 

#Dimensões do Cano
LARGURA_CANO = 80
ALTURA_CANO = 500

ESPACO_CANOS = 150         #Espaço entre o cano de cima e o debaixo

#=======================================Sprites===================================================
FUNDO = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "fundo.png")), (LARGURA, ALTURA - 112))

PASSARO_UP = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "bluebird-upflap.png")), (34*1.5, 24*1.5))
PASSARO_MEIO = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "bluebird-midflap.png")), (34*1.5, 24*1.5))
PASSARO_BAIXO = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "bluebird-downflap.png")), (34*1.5, 24*1.5))

CANO = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "cano.png")), (LARGURA_CANO, ALTURA_CANO))
BASE = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "base.png")), (LARGURA_CHAO, ALTURA_CHAO))

GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "gameover.png")), (192*1.25, 42*1.25)) 
RESTART = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "restart.png")), (120*1.25, 42*1.25))
NOME = pygame.image.load(os.path.join("Sprites", "nome.png")) 

#==================================================================================================

#Título do jogo e criação da janela
pygame.display.set_caption("Flappy Bird")
JANELA = pygame.display.set_mode((LARGURA, ALTURA))

class Passaro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cria uma lista e adiciona os sprite do passaro nela
        self.sprites = []
        self.sprites.append(PASSARO_UP)
        self.sprites.append(PASSARO_MEIO)
        self.sprites.append(PASSARO_BAIXO)

        #Serve para controlar a velocidade do movimento do pássaro
        self.contador = 0
        self.vel_pass = 0

        self.imagem_atual = 0
        self.image = self.sprites[self.imagem_atual]
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA/2 - 150, ALTURA/2)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):

        #O pássaro só começa a cair depois de apertar a "Barra de Espaço"
        if voando == True:
            #Queda no chão (Gravidade)
            self.vel_pass += 0.5
            if self.vel_pass > 8:
                self.vel_pass = 8               #Limita a velocidade de queda do pássaro
            if self.rect.bottom < ALTURA - ALTURA_CHAO:         #Toda vez que a parte debaixo do pássaro chegar no chão
                self.rect.y += int(self.vel_pass)

        if game_over == False:
            #Contador para controlar o movimento do pássaro com base na batida da asa
            self.contador += 1
            asa_bate = 5

            if self.contador > asa_bate:
                self.contador = 0
                '''
                Incrementa mais um na lista, e verifica se passa do numero de elementos da lista sprite,
                se passar volta a ser zero e continua a incrementar (faz o pássaro se mover)
                '''
                self.imagem_atual += 1           #Faz o pássaro se mover
                if self.imagem_atual >= len(self.sprites):
                    self.imagem_atual = 0
            self.image = self.sprites[self.imagem_atual]

            #Rotação do Pássaro no seu próprio eixo
            '''
            A Função rotate, controla a rotação do objeto, por padrão o giro é no sentido anti-horário, 
            para inverter, ou seja, sentido horário é necessário um valor negativo
            '''
            self.image = pygame.transform.rotate(self.sprites[self.imagem_atual], self.vel_pass*-2)

    def pulo(self):
        if game_over == False:
            self.vel_pass = -10
            som_asa.play()

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = BASE
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 336                 # 336 é a largura do sprite da base 
        self.rect.y = ALTURA - ALTURA_CHAO        # 112 é a altura do sprite da base
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if game_over == False:
            self.rect.x -= scroll_vel

class Cano(pygame.sprite.Sprite):
    def __init__(self, x, y, invertido):
        pygame.sprite.Sprite.__init__(self)
        self.image = CANO
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        #Inverte a posição dos canos, posição 1 é invertido e -1 é para cima (posição normal) 
        if invertido == 1:
            self.image = pygame.transform.flip(self.image, False, True)      #O False ou True indicam qual eixo eu quero inverter o x ou o y
            self.rect.bottomleft = [x, y - int(ESPACO_CANOS//2)]
        if invertido == -1:
            self.rect.topleft = [x, y + int(ESPACO_CANOS//2)]

    def update(self):
        if game_over == False:
            self.rect.x -= scroll_vel         #Movimenta os canos
            #Apaga os canos depois que desaparecem da tela
            if self.rect.right < 0:
                self.kill()

class Botao():
    def __init__(self, x, y, imagem):
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.click = False

    def draw(self):

        game_play = False

        #Pega o posição do mouse
        pos = pygame.mouse.get_pos()

        #Verifica se o mouse está sob o botão
        if self.rect.collidepoint(pos):
            ''' 
            O número entre colchetes significa o índice dos botões do mouse, 
            0 é o botão esquerdo e 1 significa que ele foi clicado
            '''
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                game_play = True
            
        JANELA.blit(self.image, (self.rect.x, self.rect.y))

        return game_play

#Função para escrever na tela
def texto_jogo(msg, cor, tam, x, y):
    FONTE = pygame.font.Font("Fontes/Retro Gaming/Retro-Gaming.ttf", tam)
    texto = FONTE.render(msg, True, cor)
    JANELA.blit(texto, texto.get_rect(center = [x, y]))


#==========================Sons do Jogo======================
som_pontos = pygame.mixer.Sound(os.path.join("Sons", "point.wav")) 
som_batida = pygame.mixer.Sound(os.path.join("Sons", "hit.wav"))
som_asa = pygame.mixer.Sound(os.path.join("Sons", "wing.wav"))

scroll_base = 0            #Velocidade com que a base irá se mover
scroll_vel = 4             #Velocidade com que os objetos na tela irão andar
freq_canos = 1000          #Frequência com que os canos irão aparecer (milissegundos)
ultimo_cano = pygame.time.get_ticks() - freq_canos    #Função para obter o tempo em milissegundos
pontos = 0

#Cria o Botão do Restart
botao_restart = Botao(LARGURA//2, ALTURA//2, RESTART)

relogio = pygame.time.Clock()
FPS = 60

run = True
voando = False
atravessar_cano = False
game_over = False
som_play = True

#===================Grupo dos Pássaros==========================
passaro_grupo = pygame.sprite.Group()            #Armazena os sprites
passaro = Passaro()                              #Instanciar o objeto pássaro                       
passaro_grupo.add(passaro)
#===============================================================

#===================Grupo do Chão===============================
#Calcula quantos chãos cabem na janela  336*2 = 672
chao_grupo = pygame.sprite.Group()
for i in range(LARGURA_CHAO//2):
    chao = Chao(i)
    chao_grupo.add(chao)

#===================Grupo dos Canos=============================
cano_grupo = pygame.sprite.Group()

while run:

    relogio.tick(FPS)

    #Desenha o Background
    JANELA.blit(FUNDO, (0,0))   
        
    #Desenha o grupo de passaro
    passaro_grupo.draw(JANELA)

    #Desenha o grupo de canos
    cano_grupo.draw(JANELA)

    #Desenha o grupo do chao
    chao_grupo.draw(JANELA)

    if voando == True and game_over == False: 
        #Gera os canos normais e invertidos 
        tempo_cano = pygame.time.get_ticks()
        if tempo_cano - ultimo_cano > freq_canos:
            cano_altura = random.randint(-100, 100)    #Cria o espaço entre o cano debaixo e o de cima 
            cano_normal = Cano(LARGURA, ALTURA//2 + cano_altura, -1)
            cano_invertido = Cano(LARGURA, ALTURA//2 + cano_altura, 1)
            cano_grupo.add(cano_normal)
            cano_grupo.add(cano_invertido)
            ultimo_cano = tempo_cano

    '''
    Verifica os pontos - quando o pássaro passar pelo canto superior esquerdo do cano,
    e chegar no lado superior direito do cano sem colidir será computado um ponto
    '''
    if len(cano_grupo) > 0:
        if (passaro_grupo.sprites()[0].rect.left > cano_grupo.sprites()[0].rect.left) and (passaro_grupo.sprites()[0].rect.right < cano_grupo.sprites()[0].rect.right) and (atravessar_cano == False):
            atravessar_cano = True
        if atravessar_cano == True:
            if passaro_grupo.sprites()[0].rect.left > cano_grupo.sprites()[0].rect.right:
                pontos += 1
                som_pontos.play()
                atravessar_cano = False

    #Escreve os pontos na tela
    texto_jogo(str(pontos), (255,255,255), 40, LARGURA//2, ALTURA//2 - 300)
    
    #Game Over     
    if (pygame.sprite.groupcollide(passaro_grupo, chao_grupo, False, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(passaro_grupo, cano_grupo, False, False, pygame.sprite.collide_mask)):
        game_over = True
        if som_play:
            som_play = False 
            som_batida.play()
            
            #Game Over e Restart
            while game_over:
               
                JANELA.blit(GAME_OVER, (LARGURA//2 - 100, ALTURA//2 - 200))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    
                if botao_restart.draw() == True:        
                    
                    #Cria o Botão do Restart
                    botao_restart = Botao(LARGURA//2, ALTURA//2, RESTART)
                    
                    cano_grupo.empty()
                    passaro.rect.x = LARGURA/2 - 150 
                    passaro.rect.y = ALTURA/2

                    #==========================Sons do Jogo======================
                    som_pontos = pygame.mixer.Sound(os.path.join("Sons", "point.wav")) 
                    som_batida = pygame.mixer.Sound(os.path.join("Sons", "hit.wav"))
                    som_asa = pygame.mixer.Sound(os.path.join("Sons", "wing.wav"))

                    scroll_base = 0            #Velocidade com que a base irá se mover
                    scroll_vel = 4             #Velocidade com que os objetos na tela irão andar
                    freq_canos = 1000          #Frequência com que os canos irão aparecer (milissegundos)
                    ultimo_cano = pygame.time.get_ticks() - freq_canos    #Função para obter o tempo em milissegundos
                    pontos = 0

                    relogio = pygame.time.Clock()
                    FPS = 60

                    run = True
                    voando = False
                    atravessar_cano = False
                    game_over = False
                    som_play = True

                pygame.display.update()

    if voando == False:  
        JANELA.blit(NOME, (LARGURA//2 - 180, ALTURA//2 - 160))
        texto_jogo("Press SPACE to Play", (255,255,255), 30, LARGURA//2, ALTURA//2 + 160)

    #Loop Principal
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                voando = True
                passaro.pulo()

    #Atualiza o grupo de passaros      
    passaro_grupo.update()

    #Atualiza o grupo de canos     
    cano_grupo.update()

    #Chama o grupo do chao
    chao_grupo.update()
    
    pygame.display.update()

