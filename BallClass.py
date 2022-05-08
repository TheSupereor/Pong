import pygame
import consts
import random
import PlayerClass


class Ball:
    def __init__(self, screen):
        self.ball_object = pygame.Rect(consts.LARGURA / 2 - 15, consts.ALTURA / 2 - 15, 30, 30)
        self.draw_ball(screen)

    def position_ball(self, opponent, player, dt, screen):
        self.ball_object.x += consts.BALL_X_SPEED * dt
        self.ball_object.y += consts.BALL_Y_SPEED * dt

        # evitar grudar no teto
        if -0.1 < consts.BALL_X_SPEED < 0.1:
            consts.BALL_X_SPEED = consts.BALL_X_SPEED * 2

        # colisão nos limites da tela cima e baixo
        if self.ball_object.top <= 0 or self.ball_object.bottom >= consts.ALTURA:
            consts.BALL_Y_SPEED *= -1

        # problema dos campos da tela
        # pontuação direita e esquerda
        if self.ball_object.left >= consts.LARGURA:
            opponent.score(screen)
            self.reset_ball()
        elif self.ball_object.right <= 0:
            player.score(screen)
            self.reset_ball()

        # colisão nos jogadores
        if self.ball_object.bottom >= opponent.opponent_object.top and self.ball_object.top <= \
                opponent.opponent_object.bottom and self.ball_object.left <= opponent.opponent_object.right:
            delta = self.ball_object.centery - opponent.opponent_object.centery
            consts.BALL_Y_SPEED = delta * 0.01
            consts.BALL_X_SPEED *= -1
        if self.ball_object.bottom >= player.player_object.top and self.ball_object.top <= player.player_object.bottom \
                and self.ball_object.right >= player.player_object.left:
            delta = self.ball_object.centery - player.player_object.centery
            consts.BALL_Y_SPEED = delta * 0.01
            consts.BALL_X_SPEED *= -1

    def draw_ball(self, screen):
        pygame.draw.ellipse(screen, (200, 200, 200), self.ball_object)

    def reset_ball(self):
        self.ball_object.center = (consts.LARGURA/2, consts.ALTURA/2)
        consts.BALL_X_SPEED = random.choice((-0.5, 0.5))
        consts.BALL_Y_SPEED = random.choice((-0.5, 0.5))

    def increase_dificulty(self, dificulty_increase):
        consts.BALL_X_SPEED += dificulty_increase
        consts.BALL_Y_SPEED += dificulty_increase

    def reset(self):
        self.ball_object = None

