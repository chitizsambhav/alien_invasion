import sys

import pygame

from settings import Settings

from ship import Ship

screen_settings = Settings()


def check_key_down(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True


def check_key_up(event, ship):
    ship.moving_right = False
    ship.moving_left = False


def check_event(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            check_key_up(event, ship)
        elif event.type == pygame.KEYDOWN:
            check_key_down(event, ship)


def update_screen(ai_settings, ship, screen):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    pygame.display.flip()
