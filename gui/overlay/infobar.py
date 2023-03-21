import lvgl as lv

import config
from drivers import Clock

from .bar import Bar


class InfoBar(Bar):
    """_summary_

    Args:
        lv_obj_extended (_type_): _description_
    """

    # Keep a class level instance variable
    _instance = None

    # Implement InfoBar as a singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InfoBar, cls).__new__(cls)
        return cls._instance

    # Set class level constants
    HEIGHT = 40
    KIND = "InfoBar"

    def __init__(self):
        super().__init__(height=self.HEIGHT, top=True, kind=self.KIND)

        self.timer = Clock()
        self.timer.add_subscriber(self)

        # Set the padding but offset the top and bottom
        # padding to align in the visible region
        self.set_style_pad(self.OFFSET, 0, 10, 10)
        self.set_style_bg_color(self.reader.values[config.COLOUR_PANEL], lv.PART.MAIN)
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
        self.set_layout(lv.LAYOUT_GRID.value)

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

    def update_time(self, time):
        time_str = f"{time[3]:02}:{time[4]:02}:{time[5]:02}"
        self.time_label.set_text(time_str)

    def update_title(self, title: str):
        pass
