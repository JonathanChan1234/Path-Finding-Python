import os
from typing import Tuple

import pygame
from pygame.freetype import Font
from pygame.sprite import Sprite, LayeredUpdates

from ui_utility.UIComponent import UIComponent
from ui_utility.UIManager import UIManager


class UIDialogBackground(Sprite):
    TitleMargin = 0.05
    ContentMargin = 0.2
    TitleTextSize = 0.1
    ContentTextSize = 0.05

    def __init__(self,
                 width: int,
                 height: int,
                 background: Tuple[int, int, int],
                 title: str = '',
                 title_color: Tuple[int, int, int] = (0, 0, 0),
                 title_size: int = None,
                 content: str = '',
                 content_font_color: Tuple[int, int, int] = (0, 0, 0),
                 content_font_size: int = None):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.background = background
        self.image = pygame.Surface([width, height])
        self.image.fill(self.background)
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(center=(width, height))

        # title text
        self.title = title
        self.title_size = title_size or round(UIDialogBackground.TitleTextSize * height)
        self.title_color = title_color
        title_margin = title_size if title_size else UIDialogBackground.TitleMargin * height
        x, y = self.word_wrap(self.title, self.title_size, self.title_color, title_margin)

        # content text
        self.content = content
        self.content_font_color = content_font_color
        self.content_font_size = content_font_size or round(UIDialogBackground.ContentTextSize * height)
        content_margin = y + 30
        self.word_wrap(self.content, self.content_font_size, self.content_font_color, content_margin)

    def word_wrap(self, text, size, text_color, margin):
        font = Font(None, size)
        font.origin = True
        words = text.split(' ')
        width, height = self.image.get_size()
        line_spacing = font.get_sized_height() + 2
        x, y = 0, line_spacing + margin
        space = font.get_rect(' ')
        for word in words:
            bounds = font.get_rect(word)
            if x + bounds.width + bounds.x >= width:
                x, y = 0, y + line_spacing
            if x + bounds.width + bounds.x >= width:
                raise ValueError("word too wide for the surface")
            if y + bounds.height - bounds.y >= height:
                raise ValueError("text to long for the surface")
            font.render_to(self.image, (x, y), None, text_color)
            x += bounds.width + space.width
        return x, y

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
                 background: Tuple[int, int, int],
                 title: str = '',
                 title_color: Tuple[int, int, int] = (0, 0, 0),
                 title_size: int = None,
                 content: str = '',
                 content_font_color: Tuple[int, int, int] = (0,0,0),
                 content_font_size: int = None,
                 show: bool = True):
        if height < 200:
            raise Exception('The height of UI Dialog must be larger than 200')
        if width < 200:
            raise Exception('The width of UI Dialog must be larger than 200')

        self.show = show

        # initialize components inside the UI Dialog
        self.background = UIDialogBackground(width, height, background, title, title_color, title_size, content, content_font_color, content_font_size)
        top, right = self.background.rect.topright
        self.close_button = UIDialogButton(top - UIDialogButton.BUTTON_WIDTH, right)
        LayeredUpdates.__init__(self, [self.background, self.close_button])
        UIComponent.__init__(self, manager)

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
