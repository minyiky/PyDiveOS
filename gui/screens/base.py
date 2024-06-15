import lvgl as lv

from gui import lv_obj_extended

TYPE_CHECKING = False
try:
    from typing import Protocol
    TYPE_CHECKING = True
except ImportError:
    pass

if TYPE_CHECKING:
    class Reader(Protocol):
        @property
        def SCREEN_WIDTH(self) -> int: ...
        @SCREEN_WIDTH.setter
        def SCREEN_WIDTH(self, val: int): ...

        @property
        def SCREEN_HEIGHT(self) -> int: ...
        @SCREEN_HEIGHT.setter
        def SCREEN_HEIGHT(self, val: int): ...

        @property
        def COLOUR_BG(self) -> lv.color_t: ...
        @COLOUR_BG.setter
        def COLOUR_BG(self, hex: str): ...


class Backdrop(lv_obj_extended):
    def __init__(self,reader: Reader):
        super().__init__(lv.scr_act())
        self.set_size(
            reader.SCREEN_WIDTH, reader.SCREEN_HEIGHT
        )
        self.set_style_bg_color(reader.COLOUR_BG, lv.PART.MAIN)
        self.set_style_border_width(0, lv.PART.MAIN)
        self.set_style_radius(0, lv.PART.MAIN)
