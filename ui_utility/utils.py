from typing import Tuple, List

from pygame.freetype import Font
from pygame.surface import Surface

'''
    render inline text
    render text to a single line, overflow to the next line if too long
    :param surface: surface to be rendered on
    :param text: text to be rendered
    :param size: font size of the text
    :param text_color:
    :param start_x: where to start rendering (relative to the surface), default to be 0
    :param start_y: where to start rendering (relative to the surface), default to be 0
    :rtype Tuple[int, int]
    :return x, y, where the text finished rendering
    :raise if the word is too wide (exceed the width) or the height of the rendered text exceed the height
'''


def render_inline_text(surface: Surface,
                       text: str,
                       size: int,
                       text_color: Tuple[int, int, int],
                       start_x: int = 0,
                       end_x: int = None,
                       start_y: int = 0,
                       end_y: int = None):
    width, height = surface.get_size()
    end_x = end_x or width
    end_y = end_y or height

    font = Font(None, size)
    font.origin = True

    line_spacing = font.get_sized_height() + 2
    x, y = start_x, line_spacing + start_y
    space = font.get_rect(' ')
    words = text.split(' ')

    # render word by word
    for word in words:
        bounds = font.get_rect(word)
        if x + bounds.width + bounds.x >= end_x:
            x, y = start_x, y + line_spacing
        if x + bounds.width + bounds.x >= end_x:
            raise ValueError(f"word too wide for the surface: {text}")
        if y + bounds.height - bounds.y >= end_y:
            raise ValueError(f"text to long for the surface: {text}")
        font.render_to(surface, (x, y), None, text_color)
        x += bounds.width + space.width
    return x, y


def render_multiline_text(surface: Surface,
                          text: List[str],
                          size: int,
                          text_color: Tuple[int, int, int],
                          start_x: int = 0,
                          end_x: int = None,
                          start_y: int = 0,
                          end_y: int = None):
    font = Font(None, size)
    font.origin = True
    x, y = start_x, start_y
    for line in text:
        x, y = render_inline_text(surface, line, size, text_color, start_x, end_x, y, end_y)
    return x, y
