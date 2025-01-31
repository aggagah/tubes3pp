import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Sebuah class untuk mengontrol ship"""

    def __init__(self, ai_game):
        """menginisiasi ship dan mensetting posisi awal dari ship tersebut."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # meload gambar ship dan persegi panjang
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # memulai setiap ship yang baru dengan menempatkannya di bawah dari layar
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value the ship's horizontal position.
        self.x = float(self.rect.x)

        # movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's positon based on movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        self.rect.x = self.x

    def blitme(self):
        """Menggambar ship pada posisi saat ini."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Memposisikan ship pada tengah bawah layar."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

