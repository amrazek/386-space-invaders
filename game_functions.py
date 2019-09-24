import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


# def check_key_down_events(event, ai_settings, screen, ship, bullets):
#     """Respond to key presses."""
#     if event.key == pygame.K_RIGHT:
#         # move the ship to the right
#         ship.moving_right = True
#     elif event.key == pygame.K_LEFT:
#         ship.moving_left = True
#     elif event.key == pygame.K_SPACE:
#         fire_bullet(ai_settings, screen, ship, bullets)
#     elif event.key == pygame.K_q:
#         sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limited not reached yet"""
    # create a new bullet and add it to bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


# def check_key_up_events(event, ship):
#     if event.key == pygame.K_RIGHT:
#         ship.moving_right = False
#     elif event.key == pygame.K_LEFT:
#         ship.moving_left = False
#
#
# def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
#     """Respond to keyboard and mouse events"""
#     # watch for keyboard and mouse events
#     for evt in pygame.event.get():
#         if evt.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif evt.type == pygame.KEYDOWN:
#             check_key_down_events(evt, ai_settings, screen, ship, bullets)
#
#         elif evt.type == pygame.KEYUP:
#             check_key_up_events(evt, ship)
#         elif evt.type == pygame.MOUSEBUTTONDOWN:
#             mouse_x, mouse_y = pygame.mouse.get_pos()
#             check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


# def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
#     """Start a new game when the player clicks Play."""
#     button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
#
#     if button_clicked and not stats.game_active:
#         # Reset the game settings
#         ai_settings.initialize_dynamic_settings()
#
#         # hide the mouse cursor
#         pygame.mouse.set_visible(False)
#
#         # Reset the game statistics
#         stats.reset_stats()
#         stats.game_active = True
#
#         # Reset the scoreboard images
#         sb.prep_score()
#         sb.prep_high_score()
#         sb.prep_level()
#         sb.prep_ships()
#
#         # Empty the list of aliens and bullets
#         aliens.empty()
#         bullets.empty()
#
#         # Create a new fleet and center the ship
#         create_fleet(ai_settings, screen, ship, aliens)
#         ship.center_ship()


# def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
#     # redraw screen
#     screen.fill(ai_settings.bg_color)
#
#     # Redraw all bullets behind ship and aliens
#     for bullet in bullets.sprites():
#         bullet.draw_bullet()
#
#     ship.draw_me()
#     aliens.draw(screen)
#
#     # Draw the score information
#     sb.show_score()
#
#     # Draw the play button if the game is inactive.
#     if not stats.game_active:
#         play_button.draw_button()
#
#     # make most recently drawn screen visible
#     pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)














# def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
#     """Respond to ship being hit by alien."""
#     if stats.ships_left > 0:
#         # Decrement ships_left.
#         stats.ships_left -= 1
#
#         # Update scoreboard
#         sb.prep_ships()
#
#         # Empty the list of aliens and bullets
#         aliens.empty()
#         bullets.empty()
#
#         # Create a new fleet and center the ship
#         create_fleet(ai_settings, screen, ship, aliens)
#         ship.center_ship()
#
#         # Pause
#         sleep(0.5)
#     else:
#         stats.game_active = False
#         pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
