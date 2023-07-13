from abc import ABC, abstractmethod

from data_objects import Content


class Generator(ABC):
    _name: str
    __INITIAL_PARAMS_VALUES: dict[str, str]
    _current_params_values: dict[str, str]

    @abstractmethod
    def get_output(self, params: dict[str, str]) -> Content:
        pass

    @abstractmethod
    def set_params(self, params: dict[str, str]):
        # Here we have to check if the parameters actually belong to the
        # processor
        pass
