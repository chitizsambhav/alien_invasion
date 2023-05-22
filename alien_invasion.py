import pygame
from ship import Ship
import game_functions as gf
from settings import Settings

ai_settings = Settings()


def run_game():
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
    ship = Ship(ai_settings, screen)
    pygame.display.set_caption('Alien Invasion')

    while True:
        gf.check_event(ship)
        ship.update()
        gf.update_screen(ai_settings, ship, screen)


run_game()
