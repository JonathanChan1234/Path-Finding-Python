import sys
import random
import pygame
import os
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 200
FPS = 60


class Mosquito(pygame.sprite.Sprite):
    def __init__(self, width, height, window_width, window_height):
        super().__init__()
        self.raw_image = pygame.image.load(os.path.join(os.getcwd(), 'ui/mosquito.png'))
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        self.width = width
        self.height = height
        self.window_width = window_width
        self.window_height = window_height
        random_x, random_y = self.get_random_position()
        self.x_pos = random_x
        self.y_pos = random_y
        self.rect = self.image.get_rect()
        self.rect.topleft = (random_x, random_y)

    def get_random_position(self):
        random_width = random.randint(10, self.window_width)
        random_height = random.randint(10, self.window_height)
        return random_width, random_height

    def update_random_position(self):
        # self.kill()
        random_x, random_y = self.get_random_position()
        self.x_pos = random_x
        self.y_pos = random_y
        self.rect.topleft = (self.x_pos, self.y_pos)

    def check_hit(self, x_pos, y_pos) -> bool:
        if self.x_pos <= x_pos <= self.x_pos + self.window_width \
                and self.y_pos <= y_pos <= self.y_pos + self.window_height:
            return True
        return False


class MosquitoGame:
    def __init__(self, window_width, window_height, fps):
        # Game window initialization
        pygame.init()
        self.window_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Mosquito Test")
        self.window_surface.fill(WHITE)
        self.points = 0
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.hit_text_surface = None
        self.my_font = pygame.font.SysFont(None, 30)
        self.my_hit_font = pygame.font.SysFont(None, 40)

    def refresh(self, mosquito: Mosquito):
        self.window_surface.fill(WHITE)
        text_surface = self.my_font.render('Points: {}'.format(self.points), True, (0, 0, 0))
        self.window_surface.blit(mosquito.image, mosquito.rect)
        self.window_surface.blit(text_surface, (10, 0))

        if self.hit_text_surface:
            self.window_surface.blit(self.hit_text_surface, (10, 20))
            self.hit_text_surface = None
        self.clock.tick(self.fps)

    def gain_point(self):
        self.points += 5
        self.hit_text_surface = self.my_hit_font.render('Hit!!', True, (0, 0, 0))


def get_random_position(window_width, window_height):
    random_width = random.randint(10, window_width)
    random_height = random.randint(10, window_height)
    return random_width, random_height


def main():
    mosquitoGame = MosquitoGame(WINDOW_WIDTH, WINDOW_HEIGHT, FPS)
    mosquito = Mosquito(IMAGE_WIDTH, IMAGE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
    reload_mosquito_event = USEREVENT + 1
    pygame.time.set_timer(reload_mosquito_event, 1000)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == reload_mosquito_event:
                mosquito.update_random_position()
            if event.type == MOUSEBUTTONDOWN:
                if mosquito.check_hit(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    mosquito.update_random_position()
                    mosquitoGame.gain_point()
            mosquitoGame.refresh(mosquito)
            pygame.display.update()


if __name__ == '__main__':
    main()
