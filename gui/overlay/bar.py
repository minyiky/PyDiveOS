try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Protocol

import lvgl as lv

from config import Reader

from ..base_object import lv_obj_extended

if TYPE_CHECKING:

    class Controller(Protocol):
        def foo(self) -> None:
            pass


class Bar(lv_obj_extended):
    """_summary_

    Args:
        lv_obj_extended (_type_): _description_
    """

    # Set class level constants
    OFFSET = 10  # Offset is used to hide the edge of the bar
    KIND = None

    def __init__(
            self,
            height: int,
            top: bool,
            kind: str,
            reader: Reader,
            ):
        super().__init__(lv.layer_top())

        self.type = kind
        self.controller = None
        # Setup config reader

        self.reader = reader

        # Set the normal and hidden positions of the overlay object
        mod = -1 if top else 1
        scr_height = self.reader.SCREEN_HEIGHT
        normal_pos = mod * (scr_height - height + (self.OFFSET * 2)) // 2
        hidden_pos = mod * (height + scr_height) // 2 - 1

        # Setup animations
        self._show_anim = self._create_anim(
            start=hidden_pos, end=normal_pos, path=lv.anim_t.path_overshoot
        )
        self._hide_anim = self._create_anim(start=normal_pos, end=hidden_pos)

        # Setup object properties
        self.set_width(self.reader.SCREEN_WIDTH)
        self.set_height(height)
        self.set_x(0)
        self.set_y(normal_pos)
        self.visible = True
        self.set_align(lv.ALIGN.CENTER)
        self.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)

        # Set the padding but offset the top and bottom
        # padding to align in the visible region
        top_mod, bottom_mod = (self.OFFSET, 0) if top else (0, self.OFFSET)
        self.set_style_pad(bottom_mod, top_mod, 10, 10)

        self.set_style_bg_color(self.reader.COLOUR_PANEL, lv.PART.MAIN)
        self.update_layout()

    def _create_anim(
        self,
        start: int,
        end: int,
        time: int = 200,
        path=lv.anim_t.path_linear,
        delay: int = 0,
    ) -> lv.anim_t:
        anim = lv.anim_t()
        anim.init()
        anim.set_path_cb(path)
        anim.set_time(time)
        anim.set_var(self)
        anim.set_custom_exec_cb(lambda a, v: self.set_y(v))
        anim.set_delay(delay)
        anim.set_early_apply(False)
        anim.set_values(start, end)
        return anim

    def show(self):
        if self.visible:
            return
        self.visible = True
        lv.anim_t.start(self._show_anim)

    def hide(self):
        if not self.visible:
            return
        lv.anim_t.start(self._hide_anim)
        self.visible = False

    def set_controller(self, controller: Controller):
        self.controller = controller

    def __str__(self) -> str:
        return f"{self.type} object"
