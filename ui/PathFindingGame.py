from typing import Tuple

import pygame

from ui_utility.UIDialog import UIDialog
from ui_utility.UIManager import UIManager
from ui.PathFindingGrid import PathFindingGrid
from ui_utility.UIButton import UIButton
from ui_utility.UIText import UIText

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
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
        self.clearAllObstacleButton = UIButton(self.manager, 1000, 50, (66, 245, 99), font_size=30,
                                               text="Clear All Obstacle")
        self.setMarkerButton = UIButton(self.manager, 1000, 100, (235, 64, 52), font_size=30,
                                        text="Obstacle")
        self.startPathFindButton = UIButton(self.manager, 1000, 150, (235, 225, 52), font_size=30,
                                            text="Path Finding")
        self.resetGridButton = UIButton(self.manager, 1000, 200, (50, 72, 168), font_size=30, text="Reset All")

        self.messageText = UIText(self.manager, 1000, 350, (201, 24, 4), font_size=20,
                                  text="", width=200)
        self.dialog = UIDialog(self.manager,
                               width=300,
                               height=300,
                               background=(255, 255, 255),
                               title='Path Finding Game',
                               content='Click "Select Points" to set the origin/destination, '
                                       'Click Again to select the obstacle, '
                                       'Click Reset All to Reset the grid after path finding is finished')

    def refresh(self):
        # Switch cursor in different mode
        if self.grid.select_marker:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

        # update the game background
        self.window_surface.fill(self.background)
        # render grid and other ui components
        self.grid.render(self.window_surface)
        self.manager.render(self.window_surface)

        # disable the path find button if the makers are not set
        if not self.grid.is_marker_set():
            self.startPathFindButton.set_disabled()
        else:
            self.startPathFindButton.set_enabled()

        # change the button text when in point selection mode/ obstacle selection mode
        if self.grid.select_marker:
            self.setMarkerButton.set_text('Obstacles')
        else:
            self.setMarkerButton.set_text('Points')

        # disable the clear obstacle and set maker button when the animation started
        if self.grid.is_disabled():
            self.clearAllObstacleButton.set_disabled()
            self.setMarkerButton.set_disabled()
            self.startPathFindButton.set_disabled()
        else:
            self.clearAllObstacleButton.set_enabled()
            self.setMarkerButton.set_enabled()
            self.startPathFindButton.set_enabled()

        # only enable the reset button when path finding is finished
        if self.grid.is_path_find_finished():
            self.resetGridButton.set_enabled()
        else:
            self.resetGridButton.set_disabled()

        self.clock.tick(self.fps)
        pygame.display.update()

    def event_handle(self):
        for event in pygame.event.get():
            if not self.dialog.is_show():
                self.grid.event_handler(event)
            self.manager.event_handler(event)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == UIManager.BUTTON_EVENT_ID:
                if event.component_id == self.clearAllObstacleButton.component_id:
                    self.grid.clear_all_obstacle()
                if event.component_id == self.setMarkerButton.component_id:
                    self.switch_mode()
                if event.component_id == self.startPathFindButton.component_id:
                    if not self.grid.is_marker_set():
                        self.messageText.set_text("Please select two points")
                    else:
                        self.grid.start_path_find()
                if event.component_id == self.resetGridButton.component_id:
                    self.grid.reset_grid()
                if event.component_id == self.dialog.component_id:
                    if event.event == UIDialog.CLOSE_BUTTON_CLICKED:
                        self.dialog.dismiss()

    def switch_mode(self):
        self.grid.switch_mode()


if __name__ == '__main__':
    grid = PathFindingGrid(15, 15)
    path_finding_game = PathFindingGame(WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WHITE, grid)
    while path_finding_game.running:
        path_finding_game.event_handle()
        path_finding_game.refresh()
    pygame.quit()
