import pygame.font 

class Button:

    def __init__(self, ai_game, msg):
        # inisialisasi atribut dari button
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # mengatur properti pada button
        self.width, self.height = 100, 50
        self.button_color = (244,105,169)
        self.text_color = (248,248,248)
        self.font = pygame.font.SysFont(None, 48)

        # membangun button dan memposisikannya
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # text pada button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # memunculkan text dari msg
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        