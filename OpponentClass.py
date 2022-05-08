import pygame
import consts


class Opponent:
    def __init__(self, screen):
        self.opponent_object = pygame.Rect(10, consts.ALTURA/2-70, 10, 140)
        self.match_font = pygame.font.match_font(consts.FONT)
        self.point_counter = 0
        self.draw_opponent(screen)
        self.opponent_points_text(screen)
        self.win = False

    def position_opponent(self, ball):
        # movimento automatico
        if self.opponent_object.bottom < ball.y:
            self.opponent_object.bottom += consts.OPPONENT_SPEED
        if self.opponent_object.top > ball.y:
            self.opponent_object.top -= consts.OPPONENT_SPEED
        # não sair da tela
        if self.opponent_object.bottom >= consts.ALTURA:
            self.opponent_object.bottom = consts.ALTURA
        if self.opponent_object.top <= 0:
            self.opponent_object.top = 0
        self.opponent_Y_pos = self.opponent_object.y

    def draw_opponent(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.opponent_object)
        self.opponent_points_text(screen)
        self.update_point(screen)

    def opponent_points_text(self, screen):
        font = pygame.font.Font(self.match_font, consts.FONT_SIZE - 8)
        text = font.render("Opponent Points", False, consts.BRANCO)
        text_rect = text.get_rect()
        text_rect.midtop = ((consts.LARGURA / 2) - 200, 20)
        screen.blit(text, text_rect)
        self.update_point(screen)

    def update_point(self, screen):
        font = pygame.font.Font(self.match_font, consts.FONT_SIZE)
        text = font.render(str(self.point_counter), False, consts.BRANCO)
        text_rect = text.get_rect()
        text_rect.midtop = ((consts.LARGURA / 2) - 200, 50)
        screen.blit(text, text_rect)

    def score(self, screen):
        self.point_counter += 1
        self.update_point(screen)
        self.opponent_win(screen)

    def opponent_win(self, screen):
        if self.point_counter >= 3:
            self.win = True
            self.win_text(screen)

    def win_text(self, screen):
        font = pygame.font.Font(self.match_font, consts.FONT_SIZE + 40)
        text = font.render("Opponent", False, consts.BRANCO)
        text_rect = text.get_rect()
        text_rect.midtop = ((consts.LARGURA / 2), 200)
        screen.blit(text, text_rect)

    def reset(self):
        self.opponent_object = None
