import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Sebuah class yang merepresentasikan sebuah armada alien."""

    def __init__(self, ai_game):
        """Inisiasi alien dan mengatur posisi awal mulainya."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load image alien dan atur atribut rect pada image tersebut
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # menempatkan setiap alien yang baru di pojok kiri atas layar
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # menyimpan posisi tepat horizontal dari alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """Mengembalikan True jika alien berada pada tepi layar."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        
    def update(self):
        """Menggerakkan alien ke kanan atau kiri."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        
