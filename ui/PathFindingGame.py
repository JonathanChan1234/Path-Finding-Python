import sys
from typing import List
import pygame

from ui.UIManager import UIManager
from ui.PathFindingBoard import Grid
from ui.UIButton import UIButton

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (0, 0, 0)
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
        self.point_font = pygame.font.SysFont(None, 30)

        # UI Components
        self.grid = grid
        self.manager = UIManager()
        self.clearAllObstacleButton = UIButton(self.manager, 600, 50, (66, 245, 99), font_size=30,
                                               text="Clear All Obstacle")
        self.selectOriginDestinationButton = UIButton(self.manager, 600, 100, (235, 64, 52), font_size=30,
                                                      text="Select Points")

    def refresh(self):
        self.window_surface.fill(self.background)
        text_surface = self.point_font.render(f'Points: {self.points}', True, (255, 255, 255))
        self.window_surface.blit(text_surface, (10, 10))
        self.grid.render(self.window_surface)
        self.manager.render(self.window_surface)

        self.clock.tick(self.fps)
        pygame.display.update()

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.grid.event_handler(event)
            self.manager.event_handler(event)
            if event.type == self.clearAllObstacleButton.event_id:
                print(f'Clear All Obstacle')
                self.grid.clear_all_obstacle()
            if event.type == self.selectOriginDestinationButton.event_id:
                print('Select Origin/Destination Point')
                self.switch_mode()

    def switch_mode(self):
        self.grid.switch_mode()
        if self.grid.select_point_mode:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)


if __name__ == '__main__':
    grid = Grid(20, 20)
    path_finding_game = PathFindingGame(WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WHITE, grid)
    while True:
        path_finding_game.event_handle()
        path_finding_game.refresh()
