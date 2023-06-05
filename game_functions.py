import sys

import pygame

from settings import Settings
from bullet import Bullet
from alien import Alien
from time import sleep

screen_settings = Settings()


def get_alien_no(ai_settings, screen):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space = ai_settings.screen_width - 2 * alien_width
    alien_number_x = int(available_space / (2 * alien_width))
    return alien_number_x


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_fleet_drop
    ai_settings.alien_fleet_direction *= -1


def update_aliens(aliens, ship, ai_settings, screen, bullets, stats):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, ship, screen, bullets, aliens, stats)

    alien_bottom_check(ai_settings, ship, screen, bullets, aliens, stats)


def alien_bottom_check(ai_settings, ship, screen, bullets, aliens, stats):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, ship, screen, bullets, aliens, stats)


def ship_hit(ai_settings, ship, screen, bullets, aliens, stats):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        sleep(.5)
    else:
        stats.game_active = False

def get_row_nos(alien_height, ship_height, ai_settings):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    row_nos = int(available_space_y / (2 * alien_height))
    return row_nos


def create_alien(ai_settings, screen, aliens, aliens_number, row_no):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.rect.y = alien_height + 2 * row_no * alien_height
    alien.x = alien_width + 2 * aliens_number * alien_width
    alien.rect.x = alien.x
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    alien = Alien(ai_settings, screen)
    ship_height = ship.rect.height
    alien_height = alien.rect.height
    row_nos = get_row_nos(alien_height, ship_height, ai_settings)
    for row in range(row_nos):
        for alien_number in range(get_alien_no(ai_settings, screen)):
            create_alien(ai_settings, screen, aliens, alien_number, row)


def check_key_down(event, ship, ai_settings, screen, bullets):
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, ship, screen, bullets)


def fire_bullet(ai_settings, ship, screen, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, ship, screen)
        bullets.add(new_bullet)


def check_key_up(ship):
    ship.moving_right = False
    ship.moving_left = False


def check_event(ai_settings, ship, screen, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            check_key_up(ship)
        elif event.type == pygame.KEYDOWN:
            check_key_down(event, ship, ai_settings, screen, bullets)


def update_screen(ai_settings, ship, aliens, screen, bullets):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_alien_bullet_collision(bullets, aliens, ai_settings, screen, ship)


def check_alien_bullet_collision(bullets, aliens, ai_settings, screen, ship):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)
