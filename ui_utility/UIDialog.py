import os
from typing import Tuple

import pygame

from pygame.sprite import Sprite, LayeredUpdates

from ui_utility.UIComponent import UIComponent
from ui_utility.UIManager import UIManager


class UIDialogText(Sprite):
    DEFAULT_FONT_SIZE = 20
    DEFAULT_LINE_SPACING = 5

    def __init__(self,
                 color: Tuple[int, int, int],
                 text: str = '',
                 width: int = 0,  # specific the text width
                 line_spacing: int = DEFAULT_FONT_SIZE,
                 font_size=DEFAULT_LINE_SPACING,
                 font=None):
        Sprite.__init__(self)
        self.color = color
        self.text = text
        self.width = width
        self.line_spacing = line_spacing
        self.font_size = font_size
        self.font = font



class UIDialogBackground(Sprite):
    def __init__(self, width, height, background):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.background = background
        self.image = pygame.Surface([width, height])
        self.image.fill(self.background)
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(center=(width, height))

    def event_handler(self, event, component_id):
        pass


class UIDialogButton(Sprite):
    BUTTON_HEIGHT = 20
    BUTTON_WIDTH = 20

    def __init__(self, x_pos, y_pos):
        Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(os.getcwd(), '../asset/close_button.png'))
        self.image = pygame.transform.scale(self.image, (UIDialogButton.BUTTON_WIDTH, UIDialogButton.BUTTON_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)

    def event_handler(self, event, component_id):
        if event.type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.event.post(pygame.event.Event(UIManager.BUTTON_EVENT_ID, {'component_id': component_id,
                                                                             'event': UIDialog.CLOSE_BUTTON_CLICKED}))


class UIDialog(UIComponent, LayeredUpdates):
    # event
    CLOSE_BUTTON_CLICKED = "CLOSE_BUTTON_CLICKED"

    def __init__(self,
                 manager: UIManager,
                 width: int,
                 height: int,
                 background: Tuple[int, int, int]):
        if height < 200:
            raise Exception('The height of UI Dialog must be larger than 200')
        if width < 200:
            raise Exception('The width of UI Dialog must be larger than 200')

        self.show = True

        # initialize components inside the UI Dialog
        self.background = UIDialogBackground(width, height, background)
        top, right = self.background.rect.topright
        self.close_button = UIDialogButton(top - UIDialogButton.BUTTON_WIDTH, right)
        LayeredUpdates.__init__(self, [self.background, self.close_button])

        # added to the UI Manager
        manager.add_element(self)
        self.component_id = manager.assign_id()

    def dismiss(self):
        self.show = False

    def show(self):
        self.show = True

    def is_show(self) -> bool:
        return self.show

    def event_handler(self, event):
        for sprite in self.sprites():
            child_event_handler = hasattr(sprite, 'event_handler')
            if child_event_handler and callable(sprite.event_handler):
                sprite.event_handler(event, self.component_id)
            else:
                raise Exception('All child components in UIDialog must implement event_handler function')

    def render(self, window_surface: pygame.Surface):
        if self.show:
            self.draw(window_surface)
