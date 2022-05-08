import pygame
import consts


class Player:
    def __init__(self, screen):
        self.player_object = pygame.Rect(consts.LARGURA-20, consts.ALTURA/2-70, 10, 140)
        self.match_font = pygame.font.match_font(consts.FONT)
        self.point_counter = 0
        self.draw_player(screen)
        self.player_points_text(screen)
        self.win = False

    def position_player(self):
        (x, y) = pygame.mouse.get_pos()
        self.player_object.y = y - 70
        if self.player_object.bottom > consts.ALTURA:
            self.player_object.bottom = consts.ALTURA
        if self.player_object.top < 0:
            self.player_object.top = 0
        self.player_Y_pos = self.player_object.y

    def draw_player(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.player_object)
        self.player_points_text(screen)
        self.update_point(screen)

    def player_points_text(self, screen):
        font = pygame.font.Font(self.match_font, consts.FONT_SIZE - 8)
        text = font.render("Player Points", False, consts.BRANCO)
        text_rect = text.get_rect()
        text_rect.midtop = ((consts.LARGURA / 2) + 200, 20)
        screen.blit(text, text_rect)
        self.update_point(screen)

    def update_point(self, screen):
        font = pygame.font.Font(self.match_font, consts.FONT_SIZE)
        text = font.render(str(self.point_counter), False, consts.BRANCO)
        text_rect = text.get_rect()
        text_rect.midtop = ((consts.LARGURA / 2) + 200, 50)
        screen.blit(text, text_rect)

    def score(self, screen):
        self.point_counter += 1
        self.update_point(screen)
        self.player_win(screen)

    def player_win(self, screen):
        if self.point_counter >= 3:
            self.win = True
            self.win_text(screen)

    def win_text(self, screen):
        font = pygame.font.Font(self.match_font, consts.FONT_SIZE + 40)
        text = font.render("Player", False, consts.BRANCO)
        text_rect = text.get_rect()
        text_rect.midtop = ((consts.LARGURA / 2), 200)
        screen.blit(text, text_rect)

    def reset(self):
        self.player_object = None
