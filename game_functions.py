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


def update_aliens(aliens, ship, ai_settings, screen, bullets, stats, sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, ship, screen, bullets, aliens, stats, sb)
    alien_bottom_check(ai_settings, ship, screen, bullets, aliens, stats, sb)


def alien_bottom_check(ai_settings, ship, screen, bullets, aliens, stats, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, ship, screen, bullets, aliens, stats, sb)
            break


def ship_hit(ai_settings, ship, screen, bullets, aliens, stats, sb):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        aliens.empty()
        bullets.empty()
        sb.prep_ships()
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        sleep(.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


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


def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, bullets, screen, aliens, ship, sb):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
        stats.game_active = True
        sb.prep_level()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_ships()
        ai_settings.initialize_dynmaic_settings()
        aliens.empty()
        bullets.empty()
        pygame.mouse.set_visible(False)
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()


def fire_bullet(ai_settings, ship, screen, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, ship, screen)
        bullets.add(new_bullet)


def check_key_up(ship):
    ship.moving_right = False
    ship.moving_left = False


def check_event(ai_settings, ship, screen, bullets, stats, play_button, aliens, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            check_key_up(ship)
        elif event.type == pygame.KEYDOWN:
            check_key_down(event, ship, ai_settings, screen, bullets)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, bullets, screen, aliens, ship, sb)


def update_screen(ai_settings, ship, aliens, screen, bullets, play_button, stats, sb):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    sb.draw_scoreboard()
    if not stats.game_active:
        play_button.draw_button()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_alien_bullet_collision(bullets, aliens, ai_settings, screen, ship, stats, sb)


def check_alien_bullet_collision(bullets, aliens, ai_settings, screen, ship, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open('highscore.txt', 'w') as fileobject:
            fileobject.write(str(stats.high_score))
        sb.prep_high_score()
