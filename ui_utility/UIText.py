import pygame
from pygame.font import SysFont
from typing import Tuple

from ui_utility.UIComponent import UIComponent
from ui_utility.UIManager import UIManager

FONT_SIZE = 20
LINE_SPACING = 5


class UIText(pygame.sprite.Sprite, UIComponent):
    def __init__(self,
                 manager: UIManager,
                 x_pos: int,
                 y_pos: int,
                 color: Tuple[int, int, int],
                 text='Empty Text',
                 width: int = 0,  # specific the text width
                 line_spacing: int = LINE_SPACING,
                 font_size=FONT_SIZE,
                 font=None):
        super().__init__()
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.line_spacing = line_spacing
        self.font = font
        self.font_size = font_size
        self.width = width
        self.text = text
        self.color = color

        # add element to the ui manager
        manager.add_element(self)
        self.event_id = manager.assign_id()

    def init_text_ui(self):
        # ui button surface
        ui_text_list = []
        if self.width == 0:
            ui_text_list.append(SysFont(self.font, self.font_size).render(self.text, True, self.color))
        else:
            # text[start_pointer:end_pointer-1]: characters displayed in a line
            start_pointer = 0  # character start of the line
            end_pointer = 0  # character end of the line
            while end_pointer < len(self.text):
                text_width = SysFont(self.font, self.font_size).render(self.text[start_pointer:end_pointer], True, self.color).get_width()
                if text_width >= self.width:
                    ui_text_list.append(
                        SysFont(self.font, self.font_size).render(self.text[start_pointer:(end_pointer - 1)], True, self.color))
                    start_pointer = end_pointer - 1
                else:
                    end_pointer += 1
            # Add the last text element
            ui_text_list.append(
                SysFont(self.font, self.font_size).render(self.text[start_pointer:end_pointer], True, self.color))
        return ui_text_list

    def event_handler(self, event):
        pass

    def set_text(self, text: str):
        self.text = text

    def render(self, window_surface: pygame.SurfaceType):
        text_height_offset = 0
        for index, ui_text in enumerate(self.init_text_ui()):
            text_height = ui_text.get_height()
            window_surface.blit(ui_text, (
                self.x_pos, self.y_pos + text_height_offset + (self.line_spacing if index == 0 else 0)))
            text_height_offset += text_height
