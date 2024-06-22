try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Protocol

import lvgl as lv

from config import Reader
from drivers import Clock

from ..base_object import lv_obj_extended
from .bar import Bar

if TYPE_CHECKING:
    class Controller(Protocol):
        def foo(self) -> None:
            pass


class InfoBar(Bar):
    """_summary_

    Args:
        lv_obj_extended (_type_): _description_
    """
    # Set class level constants
    HEIGHT = 40
    OFFSET = 10

    def __init__(
        self,
        reader: Reader,
        clock: Clock,
    ):
        super().__init__(
            height=self.HEIGHT,
            top=True,
            kind=self.KIND,
            reader=reader,
        )

        self.reader = reader

        self.timer = clock
        self.timer.add_subscriber(self)

        normal_pos = (
            -(
                self.reader.SCREEN_HEIGHT
                - self.HEIGHT
                + (self.OFFSET * 2)
            )
            // 2
        )
        hidden_pos = -(self.HEIGHT + self.reader.SCREEN_HEIGHT) // 2 - 1

        # Setup animations
        self._show_anim = self._create_anim(
            start=hidden_pos, end=normal_pos, path=lv.anim_t.path_overshoot
        )
        self._hide_anim = self._create_anim(start=normal_pos, end=hidden_pos)

        # Setup object properties
        self.set_width(self.reader.SCREEN_WIDTH)
        self.set_height(self.HEIGHT)
        self.set_x(0)
        self.set_y(normal_pos)
        self.visible = True
        self.set_align(lv.ALIGN.CENTER)
        self.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)

        # Set the padding but offset the top and bottom
        # padding to align in the visible region
        self.set_style_pad(self.OFFSET, 0, 10, 10)
        self.set_style_bg_color(self.reader.COLOUR_PANEL, lv.PART.MAIN)
        self.update_layout()

        # Setup layout
        col_dsc = [
            lv.grid_fr(1),
            lv.grid_fr(1),
            lv.grid_fr(1),
            lv.GRID_TEMPLATE_LAST,  # type: ignore
        ]
        row_dsc = [lv.grid_fr(1), lv.GRID_TEMPLATE_LAST]  # type: ignore
        self.set_style_grid_column_dsc_array(col_dsc, 0)
        self.set_style_grid_row_dsc_array(row_dsc, 0)
        self.set_style_pad_column(5, 0)
        self.set_layout(lv.LAYOUT.GRID)

        self.time_label = lv.label(self)
        self.time_label.set_grid_cell(
            lv.GRID_ALIGN.START, 0, 1, lv.GRID_ALIGN.CENTER, 0, 1
        )
        self.time_label.set_text("TIME")
        self.time_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.time_label.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN)

        self.title_label = lv.label(self)
        self.title_label.set_grid_cell(
            lv.GRID_ALIGN.STRETCH, 1, 1, lv.GRID_ALIGN.CENTER, 0, 1
        )
        self.title_label.set_text("TITLE")
        self.title_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.title_label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

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
        anim.set_repeat_count(0)
        anim.set_repeat_delay(0)  # + 200
        anim.set_playback_delay(0)
        anim.set_playback_time(0)
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

    def __str__(self) -> str:
        return "InfoBar object"

    def update_time(self, time):
        time_str = f"{time[3]:02}:{time[4]:02}:{time[5]:02}"
        self.time_label.set_text(time_str)

    def update_title(self, title: str):
        pass
