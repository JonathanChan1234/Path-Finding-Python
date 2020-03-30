from typing import List
import pygame

from ui.UIComponent import UIComponent


class UIManager:
    def __init__(self):
        self.elements: List[UIComponent] = []
        self.event_id = pygame.USEREVENT

    def assign_id(self):
        self.event_id += 1
        return self.event_id

    def add_element(self, element):
        self.elements.append(element)

    def render(self, window_surface):
        for element in self.elements:
            element.render(window_surface)

    def event_handler(self, event):
        for element in self.elements:
            element.event_handler(event)
