import pygame


class Dimension:

    def __init__(self):
        pygame.init()
        self.screen_height = pygame.display.Info().current_h
        self.screen_width = pygame.display.Info().current_w
