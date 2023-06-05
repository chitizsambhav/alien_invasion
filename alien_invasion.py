import pygame
from ship import Ship
import game_functions as gf
from settings import Settings
from pygame.sprite import Group
from dimension import Dimension


def run_game():
    pygame.init()
    dimensions = Dimension()
    ai_settings = Settings()
    screen = pygame.display.set_mode((dimensions.screen_width, dimensions.screen_height))
    ship = Ship(ai_settings, screen)
    pygame.display.set_caption('Alien Invasion')
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)
    while True:
        gf.check_event(ai_settings, ship, screen, bullets)
        ship.update()
        gf.update_bullets(bullets, aliens, ai_settings, screen, ship)
        gf.update_aliens(aliens, ai_settings)
        gf.update_screen(ai_settings, ship, aliens, screen, bullets)


run_game()
