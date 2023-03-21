import lvgl as lv
import uasyncio
import utime

import config
from drivers.display import Unix
from gui import Controller, base_object


async def allower(interval: int):
    """A function designed implented to get around a potential bug in the
    unix port of micropython.

    When running any async process alongside lvgl any sleep greater than 49ms
    cause a hang and ne
    """
    while 1:
        await uasyncio.sleep_ms(interval)


async def main():
    lv.init()
    reader = config.Reader()
    _ = Unix(reader.values[config.SCREEN_HEIGHT], reader.values[config.SCREEN_WIDTH], 3)
    controller = Controller()
    scr = base_object.lv_obj_extended(lv.scr_act())
    scr.set_size(
        reader.values[config.SCREEN_WIDTH], reader.values[config.SCREEN_HEIGHT]
    )
    scr.set_style_bg_color(reader.values[config.COLOUR_BG], lv.PART.MAIN)
    scr.set_style_border_width(0, lv.PART.MAIN)
    scr.set_style_radius(0, lv.PART.MAIN)
    uasyncio.create_task(allower(25))

    while 1:
        await uasyncio.sleep(3)
        controller.show_top_layer()
        await uasyncio.sleep(3)
        controller.hide_top_layer()


if __name__ == "__main__":
    uasyncio.run(main())
