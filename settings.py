import random
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """initalize the game's settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.color = [(33,33,33), (117,117,117), (96,125,139), (216,27,96)]
        self.bg_color = random.choice(self.color)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,179,0)
        self.bullets_allowed = 5

        # aliens settings
        self.fleet_drop_speed = 10

        # kecepatan dari game
        self.speedup_scale = 1.1
        # kecepatan kenaikan poin
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """pengaturan awal dari objek pada game."""
        self.ship_speed = 3
        self.bullet_speed = 5
        self.alien_speed = 1.0

        # gerakan awal dari alien
        self.fleet_direction = 1

        # scoring (saat menembak alien, kita dapat score 50)
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

        