import os
from typing import Tuple, List

import numpy as np
import pygame.surfarray as surfarray
from pygame.event import Event
from pygame.sprite import Sprite, Group
from pygame import Surface, event as PyEvent, mouse, MOUSEBUTTONDOWN, image, transform, draw as PyDraw

from ui_utility.UIComponent import UIComponent
from ui_utility.UIManager import UIManager
from ui_utility.utils import render_inline_text, render_multiline_text


class UIDropdownMenu(Group, UIComponent):
    ON_VALUE_CHANGED = 'ON_VALUE_CHANGED'

    def __init__(self,
                 manager: UIManager,
                 x_pos: int,
                 y_pos: int,
                 width: int,
                 height: int,
                 options: List[str],
                 background: Tuple[int, int, int] = (255, 255, 255),
                 text_size: int = 20,
                 text_color: Tuple[int, int, int] = (0, 0, 0)):
        if len(options) == 0:
            raise Exception("There must be one or more options")
        UIComponent.__init__(self, manager)
        Group.__init__(self)

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.options = options
        self.background = background
        self.text_size = text_size
        self.text_color = text_color
        self.menu_open = False
        self.value = self.options[0]
        self.close()

    def close(self):
        self.menu_open = False
        self.empty()
        selector = self.Selector(self.x_pos, self.y_pos, self.width, self.height, self.background, self.text_size,
                                 self.text_color, self.value)
        self.add(selector)
        self.add(self.SelectorArrow(self.width, self.x_pos, self.y_pos, self.value))

    def open(self):
        self.menu_open = True
        self.empty()
        selector = self.Selector(self.x_pos, self.y_pos, self.width, self.height, self.background, self.text_size,
                                 self.text_color, self.value)
        self.add(selector)
        self.add(self.SelectorArrow(self.width, self.x_pos, self.y_pos, self.value))
        for option in self.options:
            y_pos = selector.rect.bottom + UIDropdownMenu.Selector.BORDER_MARGIN
            selector = self.Selector(self.x_pos, y_pos, self.width, self.height, self.background, self.text_size,
                                     self.text_color, option)
            self.add(selector)

    def event_handler(self, event):
        # When the menu is open, set the selected value and close the menu
        # When the menu is closed, open the menu
        for sprite in self.sprites():
            if sprite.rect.collidepoint(mouse.get_pos()) \
                    and event.type == MOUSEBUTTONDOWN:
                if self.menu_open:
                    if not sprite.value:
                        raise Exception("Invalid option clicked, Selector class does not have the property option")
                    self.value = sprite.value
                    PyEvent.post(Event(UIManager.BUTTON_EVENT_ID, {
                        'component_id': self.component_id,
                        'event': UIDropdownMenu.ON_VALUE_CHANGED,
                        'value': self.value
                    }))
                    self.close()
                    return
                else:
                    self.open()
                    return
        # close the menu when outside the menu is clicked
        if event.type == MOUSEBUTTONDOWN and self.menu_open:
            self.close()

    def render(self, window_surface):
        self.draw(window_surface)

    class Selector(Sprite):
        TEXT_RATIO_TO_SURFACE = 0.8
        BORDER_MARGIN = 10

        def __init__(self,
                     x_pos: int,
                     y_pos: int,
                     width: int,
                     height: int,
                     background: Tuple[int, int, int],
                     text_size: int,
                     text_color: Tuple[int, int, int],
                     value: str):
            Sprite.__init__(self)
            self.value = value
            self.image = Surface([width, height])
            self.image.fill(background)
            image_array = np.array(surfarray.array3d(self.image))
            image_array[:, :5, :] = np.zeros((1, 1, 1))
            image_array[:, -5:, :] = np.zeros((1, 1, 1))
            image_array[:5, :, :] = np.zeros((1, 1, 1))
            image_array[-5:, :, :] = np.zeros((1, 1, 1))
            border_image = surfarray.make_surface(image_array)
            self.image = border_image
            x, y = render_inline_text(self.image, value, text_size, text_color,
                                      start_x=UIDropdownMenu.Selector.BORDER_MARGIN, end_x=round(width * 0.8),
                                      start_y=UIDropdownMenu.Selector.BORDER_MARGIN,
                                      end_y=height - UIDropdownMenu.Selector.BORDER_MARGIN)
            self.rect = self.image.get_rect()
            self.rect.topleft = (x_pos, y_pos)
            self.rect.height = y

    class SelectorArrow(Sprite):
        ARROW_RATIO_TO_SELECTOR = 0.2

        def __init__(self, width, x_pos, y_pos, value):
            Sprite.__init__(self)
            # size of the dropdown menu arrow is 0.2 of the width of the menu
            dropdown_arrow_length = round(width * UIDropdownMenu.SelectorArrow.ARROW_RATIO_TO_SELECTOR)

            self.image = image.load(os.path.join(os.getcwd(), '../asset/dropdown_arrow.png'))
            self.image = transform.scale(self.image, (dropdown_arrow_length, dropdown_arrow_length))
            self.rect = self.image.get_rect()
            self.rect.topleft = (
                x_pos + width * (1 - UIDropdownMenu.SelectorArrow.ARROW_RATIO_TO_SELECTOR),
                y_pos + UIDropdownMenu.Selector.BORDER_MARGIN)
            self.value = value
