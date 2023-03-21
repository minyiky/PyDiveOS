from .base_object import lv_obj_extended

MAIN = "Main"
SETTINGS = "Settings"
TIME = "Time"
PLAN = "Plan"
DIVE = "Dive"

BACK = "Back"
CLOSE = "Close"


class MenuItem:
    def __init__(
        self, children: "list[str]", parent: str, screen: lv_obj_extended = None
    ):
        self.children = children
        self.parent = parent
        self.screen = screen


nav_menu = {
    MAIN: MenuItem([SETTINGS, PLAN, DIVE], None, None),
    SETTINGS: MenuItem([TIME], MAIN, None),
    TIME: MenuItem(None, SETTINGS, None),
    PLAN: MenuItem(None, MAIN, None),
    DIVE: MenuItem(None, MAIN, None),
}
