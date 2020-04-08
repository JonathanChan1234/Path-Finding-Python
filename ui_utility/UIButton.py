import pygame
from typing import Tuple

from pygame.sprite import Sprite
from ui_utility.UIComponent import UIComponent
from ui_utility.UIManager import UIManager

PADDING = 10


class UIButton(Sprite, UIComponent):
    def __init__(self,
                 manager: UIManager,
                 x_pos: int,
                 y_pos: int,
                 color: Tuple[int, int, int],
                 width: int = None,
                 height: int = None,
                 text='Test Button',
                 disable=False,
                 font_size=15,
                 padding=PADDING):
        Sprite.__init__(self)
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
        self.ui_text, self.button, self.button_rect = self.ui_components()

    # obtain all the components inside the UI button
    def ui_components(self):
        ui_text = pygame.font.SysFont(None, self.font_size).render(self.text, True, (0, 0, 0))
        text_width, text_height = ui_text.get_size()
        self.width = self.width or (text_width + self.padding)
        self.height = self.height or (text_height + self.padding)
        button = pygame.Surface([self.width, self.height])
        button.fill(self.color)
        button_rect = button.get_rect()
        button_rect.topleft = (self.x_pos, self.y_pos)
        return ui_text, button, button_rect

    def set_text(self, text: str):
        self.text = text

    def set_disabled(self):
        self.disable = True

    def set_enabled(self):
        self.disable = False

    def event_handler(self, event):
        # Ignore all the action when disabled
        if self.disable:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and \
                self.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.event.post(pygame.event.Event(UIManager.BUTTON_EVENT_ID, {'component_id': self.component_id}))

    def render(self, window_surface: pygame.SurfaceType):
        self.ui_text, self.button, self.button_rect = self.ui_components()
        text_width, text_height = self.ui_text.get_size()
        window_surface.blit(self.button, self.button_rect)
        x_offset = (self.width - text_width) / 2
        y_offset = (self.height - text_height) / 2
        if self.disable:
            self.button.set_alpha(100)
        else:
            self.button.set_alpha(255)
        window_surface.blit(self.ui_text, (x_offset + self.x_pos, y_offset + self.y_pos))
