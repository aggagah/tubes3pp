import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # Membuat instance untuk menyimpan statistik game dan membuat papan score
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # membuat play button
        self.play_button = Button(self, 'Play')
        
    def run_game(self):
        """ Start the main loop for the game."""
        # Membuat menu
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


    def _check_events(self):
        """merespon keyboard press dan mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset setting game
            self.settings.initialize_dynamic_settings()

            # reset statistik game
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # menghapus sisa objek pada game sebelumnya
            self.aliens.empty()
            self.bullets.empty()

            # mereset posisi
            self._create_fleet()
            self.ship.center_ship()  

            # menyembunyikan kursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Merespon ketika peluru bertabrakan dengan alien."""
        # merespon setiap peluru dengan alien yang telah bertabrakan.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            
            # hancurkan peluru yang sudah ada dan buat armada baru
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # naikkan level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Cek jika armada berada pada tepi layar,
        maka update posisi dari semua alien pada armada.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # melihat pada tabrakan antara alien dengan kapal
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # melihat apakah ada alien yang menyentuh atau menabrak bagian bawah dari layar
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Cek apakah ada setiap alien telah mencapai bagian bawah dari layar."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # lakukan hal yang sama seperti ketika kapal ditabrak
                self._ship_hit()
                break
    
    def _ship_hit(self):
        """Merespon ketika ship sedang ditabrak oleh alien."""
        if self.stats.ships_left > 0:
            # pengurangan ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # membuang setiap alien dan peluru yang tersisa
            self.aliens.empty()
            self.bullets.empty()

            # membuat armada alien baru dan menempatkan ship baru pada tengah bawah layar
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Membuat armada alien."""
        # membuat sebuah alien dan mencari nomor dari aliens dalam sebuah baris
        # jarak antar alien setara dengan lebar sebuah alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_height)

        # menentukan jumlah baris alien yang memenuhi layar
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # membuat armada alien yang penuh
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """membuat alien dan menempatkannya pada baris"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """respon sewajarnya jika ada alien yang telah mencapai tepi layar."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Menjatuhkan seluruh armada dan mengubah arah dari armada tersebut."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """update image on the screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Munculkan informasi score
        self.sb.show_score()

        # Munculkan play button jika game sedang tidak aktif
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    """make a game instance, and run the game."""
    ai = AlienInvasion()
    ai.run_game()
    