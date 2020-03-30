"""
Abstract Class of UI Component
"""


class UIComponent:
    def __init__(self):
        print("create ui component")

    def render(self, window_surface):
        pass

    def event_handler(self, event):
        pass
