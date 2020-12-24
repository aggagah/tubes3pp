import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Sebuah class untuk memanage tembakan peluru dari ship"""

    def __init__(self, ai_game):
        """membuat objek peluru pada posisi ship saat ini."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color


        # membuat peluru rect pada posisi (0,0) kemudian menempatkannya pada posisi yang benar
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # menyimpan posisi peluru sebagai sebuah nilai desimal
        self.y = float(self.rect.y)

    def update(self):
        """Menggerakan peluru ke atas layar."""
        # update posisi desimal dari peluru
        self.y -= self.settings.bullet_speed
        # update posisi rectangle
        self.rect.y = self.y

    def draw_bullet(self):
        """menggambar peluru ke layar."""
        pygame.draw.rect(self.screen, self.color, self.rect)