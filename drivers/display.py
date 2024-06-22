import lvgl as lv
# import SDL
from lv_utils import event_loop


class Display:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width


class Unix(Display):
    def __init__(self, height: int, width: int, zoom: float) -> None:
        super().__init__(height, width)

        self.event_loop = event_loop()
        self.disp_drv = lv.sdl_window_create(self.width, self.height)
        self.indev_drv = lv.sdl_mouse_create()
        lv.sdl_window_set_zoom(self.disp_drv, zoom)
