import lvgl as lv
import uasyncio
import utime

import config
from drivers import Clock, GasList
from drivers.display import Unix
from gui import Controller, base_object, menu, screens
from gui.overlay import InfoBar, MenuBar


async def allower(interval: int):
    """A function designed implemented to get around a potential bug in the
    unix port of micropython.

    When running any async process alongside lvgl any sleep greater than 49ms
    cause a hang
    """
    while 1:
        await uasyncio.sleep_ms(interval)


async def main():
    lv.init()

    reader = config.Reader()

    _ = Unix(reader.SCREEN_HEIGHT, reader.SCREEN_WIDTH, reader.SCREEN_ZOOM)

    scr = screens.Backdrop(
        reader
    )

    clock = Clock()

    gas_list = GasList(
        reader=reader,
    )

    info_bar = InfoBar(
        reader=reader,
        clock=clock,
    )

    menu_bar = MenuBar(
        reader=reader,
    )

    controller = Controller(
        info_bar=info_bar,
        menu_bar=menu_bar,
        clock=clock,
    )

    home = screens.HomeScreen(
        screen=scr,
        controller=controller,
        gas_list=gas_list,
        reader=reader,
    )

    uasyncio.create_task(allower(25))

    home.show()
    
    while 1:
        await uasyncio.sleep(3)
        controller.show_top_layer()
        await uasyncio.sleep(3)
        controller.hide_top_layer()


if __name__ == "__main__":
    uasyncio.run(main())
