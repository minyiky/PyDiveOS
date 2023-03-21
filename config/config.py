from ._values import values

COLOUR_BG = "colour_bg"
COLOUR_PANEL = "colour_panel"
COLOUR_BTN_NAV = "colour_btn_nav"
COLOUR_BTN_FOCUS = "colour_btn_focus"
SCREEN_WIDTH = "screen_width"
SCREEN_HEIGHT = "screen_height"


class Reader(object):
    """The base singleton config reader for the PyDive OS"""

    def __new__(cls):
        """creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.reload_data()

    def reload_data(self):
        self.__values = values

    @property
    def values(self):
        return self.__values
