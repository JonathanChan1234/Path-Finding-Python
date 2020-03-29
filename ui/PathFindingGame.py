import sys
from typing import List
import pygame

from ui.PathFindingNode import Node
from ui.PathFindingBoard import Grid

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
FPS = 60


class PathFindingGame:
    def __init__(self, window_width, window_height, fps, background, grid):
        # Game window initialization
        pygame.init()
        self.window_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Path Finding Game")
        self.background = background
        self.points = 0
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.hit_text_surface = None
        self.point_font = pygame.font.SysFont(None, 30)
        self.my_hit_font = pygame.font.SysFont(None, 40)
        self.grid = grid
        # check if the initial click
        self.keydown = False

    def refresh(self):
        self.window_surface.fill(self.background)
        text_surface = self.point_font.render(f'Points: {self.points}', True, (0, 0, 0))
        self.window_surface.blit(text_surface, (10, 0))
        self.grid.render(self.window_surface)
        if self.keydown:
            self.grid.handle_hover(pygame.mouse.get_pos())

        if self.hit_text_surface:
            self.window_surface.blit(self.hit_text_surface, (10, 20))
            self.hit_text_surface = None
        self.clock.tick(self.fps)
        pygame.display.update()

    def gain_point(self):
        self.points += 5
        self.hit_text_surface = self.my_hit_font.render('Hit!!', True, (0, 0, 0))

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check whether the current clicked node is selected
                if not self.grid.check_selected_block(pygame.mouse.get_pos()):
                    self.keydown = True
                else:
                    self.grid.deselect_cell(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                self.keydown = False


if __name__ == '__main__':
    grid = Grid(10, 10)
    path_finding_game = PathFindingGame(WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WHITE, grid)
    while True:
        path_finding_game.event_handle()
        path_finding_game.refresh()
