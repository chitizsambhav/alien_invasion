import pygame
from ship import Ship
import game_functions as gf
from settings import Settings
<<<<<<< HEAD

ai_settings = Settings()
=======
from pygame.sprite import Group
from dimension import Dimension
from game_stats import Game_stats
from button import Button
>>>>>>> d6607e39d4a529ff6cccaf6dc54914cccdb40d9f


def run_game():
    pygame.init()
<<<<<<< HEAD
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
    ship = Ship(ai_settings, screen)
    pygame.display.set_caption('Alien Invasion')

    while True:
        gf.check_event(ship)
        ship.update()
        gf.update_screen(ai_settings, ship, screen)
=======
    dimensions = Dimension()
    ai_settings = Settings()
    screen = pygame.display.set_mode((dimensions.screen_width, dimensions.screen_height))
    play_button = Button(ai_settings, screen, "Play!")
    ship = Ship(ai_settings, screen)
    pygame.display.set_caption('Alien Invasion')
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)
    stats = Game_stats(ai_settings)
    while True:
        gf.check_event(ai_settings, ship, screen, bullets, stats, play_button, aliens)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship)
            gf.update_aliens(aliens, ship, ai_settings, screen, bullets, stats)
        gf.update_screen(ai_settings, ship, aliens, screen, bullets, play_button, stats)
>>>>>>> d6607e39d4a529ff6cccaf6dc54914cccdb40d9f


run_game()
