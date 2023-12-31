import logging
from abc import ABC, abstractmethod

from presentation_maker.data_objects import Topic


class Generator(ABC):
    _NAME: str
    _INITIAL_PARAMS_VALUES: dict[str, object]
    _current_params_values: dict[str, object]
    _registry = {}

    @classmethod
    def register_generator(cls, processor_name: str):
        def decorator(subclass):
            cls._registry[processor_name] = subclass
            return subclass

        return decorator

    @classmethod
    def registry(cls):
        return cls._registry

    def __init__(self, name: str = "generator"):
        self._NAME = name
        self._INITIAL_PARAMS_VALUES = {}
        self._current_params_values = {}

    @abstractmethod
    def get_output(self, topic: Topic) -> object:
        pass

    @property
    def current_params_values(self):
        return self._current_params_values

    @current_params_values.setter
    def current_params_values(self, params: dict[str, object]):
        # checking if the parameters and the type of its values are correct
        for param in params.keys():
            value = params.get(param)
            if param not in self._INITIAL_PARAMS_VALUES.keys():
                raise KeyError(f"{param} is not a parameter for this processor")

            elif not isinstance(value, type(self._INITIAL_PARAMS_VALUES[param])):
                raise TypeError(f"{value} is not suitable for {param}," +
                                f"\n {param} only takes values of type" +
                                f" {type(self._INITIAL_PARAMS_VALUES[param])}")

        # assigning the values of all parameters from the given or default
        # values
        for param in self._INITIAL_PARAMS_VALUES.keys():
            self._current_params_values[param] = \
                params.get(param, self._INITIAL_PARAMS_VALUES[param])
        logging.debug(self._current_params_values)

    @property
    def NAME(self):
        return self._NAME
