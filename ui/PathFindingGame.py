import inspect
from typing import Tuple

import pygame

from ui_utility.UIManager import UIManager
from ui.PathFindingGrid import PathFindingGrid
from ui_utility.UIButton import UIButton
from ui_utility.UIText import UIText

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (0, 0, 0)
FPS = 60


class PathFindingGame:
    def __init__(self, window_width: int, window_height: int, fps: int, background: Tuple[int, int, int],
                 grid: PathFindingGrid):
        # Game window initialization
        pygame.init()
        self.window_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Path Finding Game")
        self.background = background
        self.running = True
        self.points = 0
        self.fps = fps
        self.clock = pygame.time.Clock()

        # UI Components
        self.grid = grid
        self.manager = UIManager()
        self.titleText = UIText(self.manager, 10, 10, (255, 255, 255), 'Path Finding Game')

        self.pointText = UIText(self.manager, 10, 30, (255, 255, 255), f'Distance: {self.points}')
        self.clearAllObstacleButton = UIButton(self.manager, 600, 50, (66, 245, 99), font_size=30,
                                               text="Clear All Obstacle")
        self.setMarkerButton = UIButton(self.manager, 600, 100, (235, 64, 52), font_size=30,
                                        text="Select Points")
        self.startPathFindButton = UIButton(self.manager, 600, 150, (235, 225, 52), font_size=30,
                                            text="Path Finding")
        self.disableTestButton = UIButton(self.manager, 600, 200, (235, 64, 52), font_size=30,
                                          text="Disable All")
        self.enableTestButton = UIButton(self.manager, 600, 250, (235, 64, 52), font_size=30,
                                         text="Enable All")
        self.messageText = UIText(self.manager, 600, 300, (201, 24, 4), font_size=20,
                                  text="", width=200)

    def refresh(self):
        self.window_surface.fill(self.background)
        self.grid.render(self.window_surface)
        self.manager.render(self.window_surface)
        self.clock.tick(self.fps)
        pygame.display.update()

    def event_handle(self):
        for event in pygame.event.get():
            self.grid.event_handler(event)
            self.manager.event_handler(event)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == UIManager.BUTTON_EVENT_ID:
                if event.component_id == self.clearAllObstacleButton.component_id:
                    self.grid.clear_all_obstacle()
                if event.component_id == self.setMarkerButton.component_id:
                    self.switch_mode()
                if event.component_id == self.disableTestButton.component_id:
                    self.clearAllObstacleButton.set_disabled()
                    self.setMarkerButton.set_disabled()
                if event.component_id == self.enableTestButton.component_id:
                    self.clearAllObstacleButton.set_enabled()
                    self.setMarkerButton.set_enabled()
                if event.component_id == self.startPathFindButton.component_id:
                    if not self.grid.is_marker_set():
                        self.messageText.set_text("Please select two points")
                    else:
                        self.grid.start_path_find()

    def switch_mode(self):
        self.grid.switch_mode()
        if self.grid.select_point_mode:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)


if __name__ == '__main__':
    grid = PathFindingGrid(20, 20)
    print(inspect.getmembers(grid))

    path_finding_game = PathFindingGame(WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WHITE, grid)
    while path_finding_game.running:
        path_finding_game.event_handle()
        path_finding_game.refresh()
    pygame.quit()
