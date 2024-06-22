import lvgl as lv

from entities import Gas
from gui import Controller, lv_obj_extended

from .screen import Screen

TYPE_CHECKING = False
try:
    from typing import Protocol

    from .screen import Reader as Scr_Reader
    TYPE_CHECKING = True
except ImportError:
    pass

if TYPE_CHECKING:
    class Reader(Scr_Reader):
        @property
        def COLOUR_BG(self) -> lv.color_t: ...
        @COLOUR_BG.setter
        def COLOUR_BG(self, hex: str): ...

        @property
        def COLOUR_GAS_ENABLED(self) -> lv.color_t: ...
        @COLOUR_GAS_ENABLED.setter
        def COLOUR_GAS_ENABLED(self, hex: str): ...

        @property
        def COLOUR_GAS_DISABLED(self) -> lv.color_t: ...
        @COLOUR_GAS_DISABLED.setter
        def COLOUR_GAS_DISABLED(self, hex: str): ...


    class GasList(Protocol):
        @property
        def gas_list(self) -> list[Gas]: ...


class HomeScreen(Screen):
    def __init__(
            self,
            controller: Controller,
            gas_list: GasList,
            screen: lv_obj_extended,
            reader: Reader,
        ):
        super(HomeScreen, self).__init__(
            screen,
            reader,
        )
        self.gas_list = gas_list
        self.controller = controller
        self.reader = reader

        col_dsc = [64] * 5 + [lv.GRID_TEMPLATE_LAST] # type: ignore
        row_dsc = [30] + [35] * 6 + [lv.GRID_TEMPLATE_LAST] # type: ignore
        self.set_style_grid_column_dsc_array(col_dsc, 0)
        self.set_style_grid_row_dsc_array(row_dsc, 0)
        self.set_style_pad_column(0, lv.PART.MAIN)
        self.set_style_pad_row(0, lv.PART.MAIN)
        self.center()
        self.set_layout(lv.LAYOUT.GRID)
        self.update_layout()
        self.x_size = 320//5
        self.y_size = 240//6

    def show(self):
        gas_list = self.gas_list.gas_list

        def show_gas(loc: int, gas: Gas) -> None:
            cont = lv_obj_extended(self)
            cont.set_style_border_width(3, lv.PART.MAIN)
            cont.set_style_border_color(self.reader.COLOUR_BG, lv.PART.MAIN)
            cont.set_style_radius(0, lv.PART.MAIN)

            colour = self.reader.COLOUR_GAS_ENABLED if gas_list[i].enabled else self.reader.COLOUR_GAS_DISABLED
            cont.set_style_bg_color(colour, lv.PART.MAIN)

            cont.set_grid_cell(lv.GRID_ALIGN.STRETCH, i, 1, lv.GRID_ALIGN.STRETCH, 6, 1)

            label = lv.label(cont)
            label.set_text(str(gas_list[i]))
            label.align_to(cont,lv.ALIGN.CENTER, 0, 0)
            label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)


        for i, gas in enumerate(gas_list):
            show_gas(i, gas)
        
        self.visible = True
