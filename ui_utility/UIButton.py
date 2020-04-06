import pygame
from typing import Tuple

from ui_utility.UIComponent import UIComponent
from ui_utility.UIManager import UIManager

PADDING = 10


class UIButton(pygame.sprite.Sprite, UIComponent):
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
        super().__init__()
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos

        # ui button surface
        self.text = pygame.font.SysFont(None, font_size).render(text, True, (0, 0, 0))
        text_width, text_height = self.text.get_size()
        if width:
            self.width = width
        else:
            self.width = text_width + padding
        if height:
            self.height = height
        else:
            self.height = text_height + padding

        self.button = pygame.Surface([self.width, self.height])
        self.button.fill(color)
        self.button_rect = self.button.get_rect()
        self.button_rect.topleft = (x_pos, y_pos)
        self.disable = disable

        # add element to the ui manager
        manager.add_element(self)
        self.component_id = manager.assign_id()

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
        window_surface.blit(self.button, self.button_rect)
        text_width, text_height = self.text.get_size()
        x_offset = (self.width - text_width) / 2
        y_offset = (self.height - text_height) / 2
        if self.disable:
            self.button.set_alpha(100)
        else:
            self.button.set_alpha(255)
        window_surface.blit(self.text, (x_offset + self.x_pos, y_offset + self.y_pos))
