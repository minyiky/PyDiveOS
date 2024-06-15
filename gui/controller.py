from .overlay import InfoBar, MenuBar
from drivers import Clock

class Controller:
    def __init__(
            self,
            info_bar: InfoBar,
            menu_bar: MenuBar,
            clock: Clock,
            *args,
            **kwargs,
            ) -> None:
        self.top_layer = [info_bar, menu_bar]
        for object in self.top_layer:
            object.set_controller(self)
        super().__init__(*args, **kwargs)
        clock.start_timer()

    def hide_top_layer(self) -> None:
        for child in self.top_layer:
            child.hide()

    def show_top_layer(self) -> None:
        for child in self.top_layer:
            child.show()

    def foo(self) -> None:
        pass