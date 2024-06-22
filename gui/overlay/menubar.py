try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import List

import lvgl as lv

from config import Reader

from .. import navigation
from ..base_object import labelled_btn
from .bar import Bar


class MenuBar(Bar):
    """_summary_

    Args:
        lv_obj_extended (_type_): _description_
    """
    # Set class level constants
    HEIGHT = 60
    NAV_BTN_SIZE = 30
    KIND = "MenuBar"

    def __init__(
            self,
            reader: Reader,
        ):
        super().__init__(
            height=self.HEIGHT,
            top=False,
            kind=self.KIND,
            reader=reader,
        )

        # Setup config reader
        self.reader = reader

        self.set_style_pad(10, 10 + self.OFFSET, 10, 10)

        # Setup layout
        col_dsc = [
            self.NAV_BTN_SIZE,
            lv.grid_fr(1),
            lv.grid_fr(1),
            lv.grid_fr(1),
            self.NAV_BTN_SIZE,
            lv.GRID_TEMPLATE_LAST,  # type: ignore
        ]
        row_dsc = [lv.grid_fr(1), lv.GRID_TEMPLATE_LAST]  # type: ignore
        self.set_style_grid_column_dsc_array(col_dsc, 0)
        self.set_style_grid_row_dsc_array(row_dsc, 0)
        self.set_style_pad_column(10, 0)
        self.set_layout(lv.LAYOUT.GRID)

        # Update Layout
        self.update_layout()

        # Setup nav buttons
        self.btn_left = self._create_nav_btn(0, lv.SYMBOL.LEFT)
        self.btn_right = self._create_nav_btn(4, lv.SYMBOL.RIGHT)

        # Setup main buttons
        self.btns = [
            self._create_btn(1),
            self._create_btn(2, self.reader.COLOUR_BTN_FOCUS),
            self._create_btn(3),
        ]

        # Update Layout
        self.update_layout()

        self.btn_left.set_size(self.btn_left.get_width(), self.btn_left.get_height())
        self.btn_right.set_size(self.btn_right.get_width(), self.btn_right.get_height())
        for btn in self.btns:
            btn.set_size(btn.get_width(), btn.get_height())

        # Update Layout
        self.update_layout()

        self._current_page = navigation.MAIN
        self._index = 0
        self._set_btns()

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

    def _create_nav_btn(
        self, col: int, symbol: str = None  # type: ignore
    ) -> labelled_btn:
        btn = labelled_btn(self, symbol)
        btn.set_style_bg_color(self.reader.COLOUR_BTN_NAV, lv.PART.MAIN)
        btn.set_grid_cell(lv.GRID_ALIGN.STRETCH, col, 1, lv.GRID_ALIGN.STRETCH, 0, 1)
        return btn

    def _create_btn(
        self, col: int, colour: lv.color_t = None  # type: ignore
    ) -> labelled_btn:
        btn = labelled_btn(self, "")
        btn.set_grid_cell(lv.GRID_ALIGN.STRETCH, col, 1, lv.GRID_ALIGN.STRETCH, 0, 1)
        if colour:
            btn.set_style_bg_color(colour, lv.PART.MAIN)
        return btn

    def _set_btns(self) -> None:
        names = self._get_btn_names()
        num_btns = len(names)
        self.btns[0].visible, start = (False, 1) if num_btns == 2 else (True, 0)
        self._index %= num_btns
        for i in range(start, 3):
            index = (self._index + i - 1) % num_btns
            name = names[index]
            if i == 1:
                self.centre_btn = name
            self.btns[i].name = name

    def _get_btn_names(self) -> List[str]:
        while (page := navigation.nav_menu[self._current_page]).children is None:
            self._current_page = page.parent
        prev = navigation.CLOSE if page.parent is None else navigation.BACK
        return page.children + [prev]

    def select(self) -> None:
        self._index = 0

        if self.centre_btn == navigation.BACK:
            self._current_page = navigation.nav_menu[self._current_page].parent
            self._set_btns()
            return

        if self.centre_btn == navigation.CLOSE:
            self._current_page = navigation.MAIN
            self._set_btns()
            self.hide
            return

        if (scr := navigation.nav_menu[self._current_page].screen) is not None:
            lv.scr_load(scr)
            self.hide
            return

        self._current_page = self.centre_btn
        self._set_btns()

    def __str__(self) -> str:
        return "MenuBar object"
