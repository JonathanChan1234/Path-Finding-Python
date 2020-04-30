from typing import Tuple

import pygame

from algorithm.astar_grid import A_STAR
from algorithm.dijkstra_grid import DIJKSTRA
from ui_utility.UIDialog import UIDialog
from ui_utility.UIDropdownMenu import UIDropdownMenu
from ui_utility.UIManager import UIManager
from ui.PathFindingGrid import PathFindingGrid
from ui_utility.UIButton import UIButton
from ui_utility.UIText import UIText
from worker.async_test import AsyncAlgorithmThread

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = (162, 196, 250)
FPS = 60
ALGORITHM_LIST = [A_STAR, DIJKSTRA]


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
        self.clearAllObstacleButton = UIButton(self.manager, 1000, 50, (66, 245, 99), 150, 40, font_size=20,
                                               text="Clear Board")
        self.setMarkerButton = UIButton(self.manager, 1000, 100, (235, 64, 52), 150, 40, font_size=20,
                                        text="Obstacle")
        self.startPathFindButton = UIButton(self.manager, 1000, 150, (235, 225, 52), 150, 40, font_size=20,
                                            text="Path Finding")
        self.resetGridButton = UIButton(self.manager, 1000, 200, (50, 72, 168), 150, 40, font_size=20, text="Reset All")

        self.messageText = UIText(self.manager, 1000, 350, (201, 24, 4), font_size=20,
                                  text="", width=200)
        self.dialog = UIDialog(self.manager,
                               width=300,
                               height=300,
                               background=(255, 255, 255),
                               title='Path Finding Game',
                               content='Click "Select Points" to set the origin/destination, '
                                       'Click Again to select the obstacle, '
                                       'Click Reset All to Reset the grid after path finding is finished',
                               show=False)
        self.dropdown_menu = UIDropdownMenu(self.manager,
                                            x_pos=1000,
                                            y_pos=300,
                                            width=150,
                                            height=50,
                                            text_size=16,
                                            options=ALGORITHM_LIST)
        self.mouse_debug_text = UIText(self.manager, 1000, 0, (0, 0, 0), '')

    def refresh(self):
        self.mouse_debug_text.set_text(f'{str(pygame.mouse.get_pos()[0])}, {str(pygame.mouse.get_pos()[1])}')
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
                if event.component_id == self.dropdown_menu.component_id:
                    # change the algorithm according to the value
                    self.grid.set_algorithm(event.value)
            if event.type == AsyncAlgorithmThread.EVENT_ID:
                print(event)

    def switch_mode(self):
        self.grid.switch_mode()


if __name__ == '__main__':
    grid = PathFindingGrid(A_STAR, 15, 13)
    path_finding_game = PathFindingGame(WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BACKGROUND_COLOR, grid)
    while path_finding_game.running:
        path_finding_game.event_handle()
        path_finding_game.refresh()
    pygame.quit()
