import lvgl as lv
import ujson

COLOUR_BG = "ui/colours/bg"
COLOUR_PANEL = "ui/colours/panel"
COLOUR_BTN_NAV = "ui/colours/btn_nav"
COLOUR_BTN_FOCUS = "ui/colours/btn_focus"
COLOUR_GAS_ENABLED = "ui/colours/gas_enabled"
COLOUR_GAS_DISABLED = "ui/colours/gas_disabled"

SCREEN_WIDTH = "ui/screen/width"
SCREEN_HEIGHT = "ui/screen/height"
SCREEN_ZOOM = "ui/screen/zoom"

DIVE_GAS_LIST = "dive/gas_list"

class Reader(object):
    """The base singleton config reader for the PyDive OS"""

    _CONFIG_FILE = f"{__file__.rsplit('/', 1)[0]}/config.json"
    _config = {}

    def __new__(cls):
        """creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.reload_data()

    def reload_data(self):
        """Reloads the data from the files in the file_dict attribute.

        This method iterates over the file_dict attribute, opens each file, and loads the configuration data using ujson.
        The loaded configuration data replaces the existing configuration in the file_dict attribute.

        Args:
            self: The instance of the class.

        Returns:
            None
        """
        with open(self._CONFIG_FILE, "r") as f:
            self._config = ujson.load(f)

    def _save(self):
        """Saves the configuration data to the specified file.

        Args:
            file: The file path to save the configuration data.

        Returns:
            None
        """
        with open(self._CONFIG_FILE, 'w') as f:
            ujson.dump(self._config, f)

    def _read(self, object: str): 
        value = self._config
        for s in object.split("/"):
            value = value[s]
        return value

    def _read_int(self, object: str) -> int:
        v = self._read(object)
        return v if isinstance(v, int) else 0

    def _read_str(self, object: str) -> str:
        return str(self._read(object))

    def _read_list_str(self, object: str) -> list[str]:
        v = self._read(object)
        return v if isinstance(v, list) else []

    def _read_list_int(self, object: str) -> list[int]:
        v = self._read(object)
        return v if isinstance(v, list) else []

    def _set(self, object: str, value) -> None:
        keys = object.split("/")
        last_key = keys.pop()
        v = self._config
        for key in keys:
            try:
                v = v[key]
            except KeyError:
                v[key] = {}
                v = v[key]
        v[last_key] = value

    def _lv_color_hex(self, hex: str) -> lv.color_t:
        return lv.color_hex(int(hex))


    ############################################################################
    # Colour Settings
    ############################################################################

    @property
    def COLOUR_PANEL(self) -> lv.color_t:
        return self._lv_color_hex(self._read_str(COLOUR_PANEL))

    @COLOUR_PANEL.setter
    def COLOUR_PANEL(self, hex: str):
        self._set(COLOUR_PANEL, hex)
        self._save()

    @property
    def COLOUR_BG(self) -> lv.color_t:
        return self._lv_color_hex(self._read_str(COLOUR_BG))

    @COLOUR_BG.setter
    def COLOUR_BG(self, hex: str):
        self._set(COLOUR_BG, hex)
        self._save()

    @property
    def COLOUR_BTN_NAV(self) -> lv.color_t:
        return self._lv_color_hex(self._read_str(COLOUR_BTN_NAV))

    @COLOUR_BTN_NAV.setter
    def COLOUR_BTN_NAV(self, hex: str):
        self._set(COLOUR_BTN_NAV, hex)
        self._save()
    
    @property
    def COLOUR_BTN_FOCUS(self) -> lv.color_t:
        return self._lv_color_hex(self._read_str(COLOUR_BTN_FOCUS))
    
    @COLOUR_BTN_FOCUS.setter
    def COLOUR_BTN_FOCUS(self, hex: str):
        self._set(COLOUR_BTN_FOCUS, hex)
        self._save()

    @property
    def COLOUR_GAS_ENABLED(self) -> lv.color_t:
        return self._lv_color_hex(self._read_str(COLOUR_GAS_ENABLED))
    
    @COLOUR_GAS_ENABLED.setter
    def COLOUR_GAS_ENABLED(self, hex: str):
        self._set(COLOUR_GAS_ENABLED, hex)
        self._save()
    
    @property
    def COLOUR_GAS_DISABLED(self) -> lv.color_t:
        return self._lv_color_hex(self._read_str(COLOUR_GAS_DISABLED))
    
    @COLOUR_GAS_DISABLED.setter
    def COLOUR_GAS_DISABLED(self, hex: str):
        self._set(COLOUR_GAS_DISABLED, hex)
        self._save()

    ############################################################################
    # Screen Settings
    ############################################################################

    @property
    def SCREEN_HEIGHT(self) -> int:
        return self._read_int(SCREEN_HEIGHT)
    
    @SCREEN_HEIGHT.setter
    def SCREEN_HEIGHT(self, val: int):
        self._set(SCREEN_HEIGHT, val)
        self._save()

    @property
    def SCREEN_WIDTH(self) -> int:
        return self._read_int(SCREEN_WIDTH)
    
    @SCREEN_WIDTH.setter
    def SCREEN_WIDTH(self, val: int):
        self._set(SCREEN_WIDTH, val)
        self._save()

    @property
    def SCREEN_ZOOM(self) -> int:
        return self._read_int(SCREEN_ZOOM)
    
    @SCREEN_ZOOM.setter
    def SCREEN_ZOOM(self, val: int):
        self._set(SCREEN_ZOOM, val)
        self._save()

    ############################################################################
    # Dive Settings
    ############################################################################

    @property
    def DIVE_GAS_LIST(self) -> list[str]:
        return self._read_list_str(DIVE_GAS_LIST)

    
    @DIVE_GAS_LIST.setter
    def DIVE_GAS_LIST(self, val: list[str]):
        self._set(DIVE_GAS_LIST, val)
        self._save()

if __name__ == "__main__":
    r = Reader()
    print(r.COLOUR_BG)