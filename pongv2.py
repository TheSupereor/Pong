import pygame
import consts
import os
import BallClass
import PlayerClass
import OpponentClass


# classe do jogo geral
class Game:
    def __init__(self):
        # tela do jogo
        pygame.init()
        # audios
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((consts.LARGURA, consts.ALTURA))
        pygame.display.set_caption(consts.TITULO_JOGO)
        # limitar quadros no menu
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.playing = False
        self.end_game = False
        self.font = pygame.font.match_font(consts.FONT)
        self.load_archives()

    def new_game(self):
        # aqui onde inicializaria as sprites
        self.run()

    def run(self):
        # loop
        self.playing = True
        # quando começar a jogar inicializar os componentes do jogo
        player = PlayerClass.Player(self.screen)
        opponent = OpponentClass.Opponent(self.screen)
        ball = BallClass.Ball(self.screen)

        # musica
        pygame.mixer.music.load(os.path.join(self.dir_audio, consts.MUSICA_JOGO))
        pygame.mixer.music.play(10, 0, 100)
        pygame.mixer.music.set_volume(0.4)

        previous = pygame.time.get_ticks()
        lag = 0
        while self.playing:
            ball.increase_dificulty(consts.AUMENTO_DIFICULDADE)
            #self.clock.tick(consts.FPS)
            current = pygame.time.get_ticks()
            elapsed = current - previous
            previous = current
            lag += elapsed
            self.events()
            while lag >= consts.MS_PER_UPDATE:
                # atualizar
                self.update(player, opponent, ball, consts.MS_PER_UPDATE, self.screen)
                lag -= consts.MS_PER_UPDATE
            self.draw(player, opponent, ball)
        # quando terminar
        ball.reset()
        player.reset()
        opponent.reset()

    def events(self):
        # define eventos
        for event in pygame.event.get():
            # fechando o jogo
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.is_running = False

    def update(self, player, opponent, ball, dt, screen):
        # atualizando sprites
        player.position_player()
        opponent.position_opponent(ball.ball_object)
        ball.position_ball(opponent, player, dt, screen)
        self.win_condition(player, opponent)
        pass

    def draw(self, player, opponent, ball):
        # limpar tela e desenhar sprites
        self.screen.fill(consts.PRETO)

        player.draw_player(self.screen)
        opponent.draw_opponent(self.screen)
        ball.draw_ball(self.screen)

        pygame.display.flip()
        pass

    def load_archives(self):
        # carregar imagens e audio
        img_dir = os.path.join(os.getcwd(), 'images')
        self.dir_audio = os.path.join(os.getcwd(), 'audio')
        #self.spritesheet = os.path.join(img_dir, 'spritesheet.png')
        self.start_logo = os.path.join(img_dir, consts.LOGO_INICIAL)

        # transformando em imagem
        self.start_logo = pygame.image.load(self.start_logo).convert_alpha()

    def show_text(self, message, font_size, color, x, y):
        # mostra os textos
        font = pygame.font.Font(self.font, font_size)
        text = font.render(message, False, color)
        text_rect = text.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text, text_rect)

    def show_start_logo(self, x, y):
        start_logo_rect = self.start_logo.get_rect()
        start_logo_rect.midtop = (x, y)
        self.screen.blit(self.start_logo, start_logo_rect)

    def show_start_screen(self):
        # carregar musica
        pygame.mixer.music.load(os.path.join(self.dir_audio, consts.MUSICA_MENU_INICIAL))
        pygame.mixer.music.play(0, 0, 200)
        # mostrar logo
        self.show_start_logo(consts.LARGURA/2, -250)
        # mostrar texto
        self.show_text('Pressione qualquer botão para começar', 24, consts.BRANCO, consts.LARGURA/2, 620)
        self.show_text('Feito por The_Sups', 24, consts.OURO, consts.LARGURA/2, 900)
        pygame.display.flip()
        self.wait_player_input()

    def wait_player_input(self):
        waiting = True
        while waiting:
            self.clock.tick(consts.FPS)
            for event in pygame.event.get():
                # saindo do jogo
                if event.type == pygame.QUIT:
                    waiting = False
                    self.is_running = False
                if event.type == pygame.KEYUP:
                    waiting = False
                    pygame.mixer.music.stop()
                    #executar som de start
                    pygame.mixer.Sound(os.path.join(self.dir_audio, consts.START_GAME)).play()

    def win_condition(self, player, opponent):
        if player.win:
            self.show_gameover_screen()
        elif opponent.win:
            self.show_gameover_screen()

    def show_gameover_screen(self):
        self.playing = False
        self.end_game = True

        # musica e texto
        pygame.mixer.music.stop()
        pygame.mixer.Sound(os.path.join(self.dir_audio, consts.MUSICA_VITORIA)).play(0, 0, 100)
        self.show_text("We have a winner!!", 40, consts.OURO, consts.LARGURA / 2, (consts.ALTURA / 2))
        self.show_text("press any button to play again!!", 20, consts.OURO, consts.LARGURA/2, (consts.ALTURA/2 + 60))
        pygame.display.flip()

        while self.end_game:
            self.clock.tick(consts.FPS)
            for event in pygame.event.get():
                # saindo do jogo
                if event.type == pygame.QUIT:
                    self.end_game = False
                    self.is_running = False
                elif event.type == pygame.KEYUP:
                    self.end_game = False
                    self.playing = True
                    self.new_game()
                    pygame.mixer.music.stop()
                    #executar som de start
                    pygame.mixer.Sound(os.path.join(self.dir_audio, consts.START_GAME)).play()


g = Game()
g.show_start_screen()

while g.is_running:
    g.new_game()

