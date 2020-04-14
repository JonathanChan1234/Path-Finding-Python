import pygame
from typing import Tuple

from pygame.sprite import Sprite, Group
from pygame.surface import Surface

from ui_utility.UIComponent import UIComponent
from ui_utility.UIManager import UIManager
from ui_utility.utils import render_inline_text

PADDING = 10


class UIButton(Group, UIComponent):
    def __init__(self,
                 manager: UIManager,
                 x_pos: int,
                 y_pos: int,
                 color: Tuple[int, int, int],
                 width: int,
                 height: int,
                 text='Test Button',
                 disable=False,
                 font_size=15,
                 padding=PADDING):
        Group.__init__(self)
        UIComponent.__init__(self, manager)
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.text = text
        self.disable = disable
        self.font_size = font_size
        self.padding = padding
        self.color = color
        self.button = Sprite()
        self.button.image = Surface([width, height])
        self.button.image.fill(color)
        render_inline_text(self.button.image, self.text, self.font_size, (0, 0, 0))
        self.button.rect = self.button.image.get_rect()
        self.button.rect.topleft = (x_pos, y_pos)
        self.add(self.button)

    def set_text(self, text: str):
        self.text = text
        self.button.image.fill(self.color)
        render_inline_text(self.button.image, self.text, self.font_size, (0, 0, 0))

    def set_disabled(self):
        self.disable = True

    def set_enabled(self):
        self.disable = False

    def event_handler(self, event):
        # Ignore all the action when disabled
        if self.disable:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and \
                self.button.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.event.post(pygame.event.Event(UIManager.BUTTON_EVENT_ID, {'component_id': self.component_id}))

    def render(self, window_surface: pygame.SurfaceType):
        if self.disable:
            self.button.image.set_alpha(100)
        else:
            self.button.image.set_alpha(255)
        self.draw(window_surface)

