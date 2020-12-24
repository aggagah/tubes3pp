import pygame
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """Sebuah class untuk menampilkan informasi score."""
    def __init__(self, ai_game):
        """Inisialisasi atribute penyimpan score"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # mengatur font untuk informasi score
        self.text_color = (248,248,248)
        self.font = pygame.font.SysFont(None, 48)

        # menyiapkan inisialisasi gambar dari score
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Mengubah score menjadi gambar yang bisa ditampilkan."""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Menampilkan score pada pojok kanan atas layar
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Mengubah high score menjadi gambar yang bisa ditampilkan."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "Highest {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Menampilkan high score pada tengah atas layar
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        level_str = "Lv. {}".format(str(self.stats.level))
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Menampilkan level di bawah score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Menampilkan berapa ship yang tersisa."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
    
    def check_high_score(self):
        """cek apakah adah high score baru."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Menampilkan score, level, dan ships ke layar."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)