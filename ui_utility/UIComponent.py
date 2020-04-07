"""
Abstract Class of UI Component
"""


class UIComponent:
    def __init__(self, manager):
        manager.add_element(self)
        self.component_id = manager.assign_id()

    def render(self, window_surface):
        pass

    def event_handler(self, event):
        pass
