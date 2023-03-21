from .overlay.infobar import InfoBar
from .overlay.menubar import MenuBar


class Controller:
    def __init__(self) -> None:
        self.top_layer = [InfoBar(), MenuBar()]
        for object in self.top_layer:
            object.set_controller(self)
        super().__init__()

    def hide_top_layer(self) -> None:
        for child in self.top_layer:
            child.hide()

    def show_top_layer(self) -> None:
        for child in self.top_layer:
            child.show()

    def foo(self) -> None:
        pass
