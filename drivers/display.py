import lvgl as lv
import SDL
from lv_utils import event_loop


class Display:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width


class Unix(Display):
    def __init__(self, height: int, width: int, zoom: float) -> None:
        super().__init__(height, width)

        SDL.init(h=height, w=width, zoom=zoom, auto_refresh=False)
        self.event_loop = event_loop(refresh_cb=SDL.refresh)

        # Register SDL display driver.

        disp_buf1 = lv.disp_draw_buf_t()
        buf1_1 = bytes(width * 10)
        disp_buf1.init(buf1_1, None, len(buf1_1) // 4)
        disp_drv = lv.disp_drv_t()
        disp_drv.init()
        disp_drv.draw_buf = disp_buf1
        disp_drv.flush_cb = SDL.monitor_flush
        disp_drv.hor_res = width
        disp_drv.ver_res = height
        disp_drv.register()

        # Register SDL mouse driver

        indev_drv = lv.indev_drv_t()
        indev_drv.init()
        indev_drv.type = lv.INDEV_TYPE.POINTER
        indev_drv.read_cb = SDL.mouse_read
        indev_drv.register()
