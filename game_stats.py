class GameStats:
    """Melacak statistik dari Alien Invasion."""
    def __init__(self, ai_game):
        """Inisialisasi statistik."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Mulai Alien Invasion dalam state yang tidak aktif
        self.game_active = False

        # high score
        self.high_score = 0
    def reset_stats(self):
        """Inisialisasi statistik yang bisa berubah saat permainan."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1