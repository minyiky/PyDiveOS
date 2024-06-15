from entities import Gas

TYPE_CHECKING = False
try:
    from typing import Protocol
    TYPE_CHECKING = True
except ImportError:
    pass

if TYPE_CHECKING:
    class Reader(Protocol):
        @property
        def DIVE_GAS_LIST(self) -> list[str]: ...
        @DIVE_GAS_LIST.setter
        def DIVE_GAS_LIST(self, val: list[str]): ...

class GasList:
    def __init__(
        self,
        reader: Reader
    ):
        # TODO: Fix bug where the enabled state is not stored
        self.reader = reader
        gas_list_str = reader.DIVE_GAS_LIST
        self._gas_list = {s: Gas.from_string(s) for s in gas_list_str}

    def _update_config(self):
        self.reader.DIVE_GAS_LIST = list(self._gas_list.keys())

    def add(self, gas: Gas):
        if str(gas) in self._gas_list.keys():
            return        
        self._gas_list[str(gas)] = gas
        self._update_config()

    def update(self, gas: Gas):
        if str(gas) not in self._gas_list.keys():
            return
        self._gas_list[str(gas)] = gas
        self._update_config()

    def delete(self, gas: Gas):
        del(self._gas_list[str(gas)])
        self._update_config()
    
    @property
    def gas_list(self) -> list[Gas]:
        return list(self._gas_list.values())
