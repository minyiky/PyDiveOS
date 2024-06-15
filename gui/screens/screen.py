import lvgl as lv

from gui import lv_obj_extended

TYPE_CHECKING = False
try:
    from typing import Protocol
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


class Screen(lv_obj_extended):
    def __init__(
            self,
            parent: lv.obj | None,
            reader: Reader,
            *args,
            **kwargs
        ):
        assert parent is not None
        super(Screen, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.set_size(reader.SCREEN_WIDTH, reader.SCREEN_HEIGHT)
        self.set_style_pad_ver(0, lv.PART.MAIN)
        self.set_style_pad_hor(0, lv.PART.MAIN)
        self.set_style_radius(0, lv.PART.MAIN)
        self.set_style_border_width(1, lv.PART.MAIN)
        self.align_to(self.parent, lv.ALIGN.CENTER, 0, 0)
        self.set_style_bg_color(reader.COLOUR_BG, lv.PART.MAIN)
        self.scrollable = False
        self.visible = False

    def show(self):
        self.visible = True