from abc import ABC, abstractmethod

from data_objects import Document


class DocumentProcessor(ABC):
    language: str
    _current_params_values: dict[str, object]
    INITIAL_PARAMS_VALUES: dict[str, object]

    def __init__(self, language: str = "english"):
        self.language = language
        self.INITIAL_PARAMS_VALUES = dict()
        self._current_params_values = dict()

    @abstractmethod
    def process_text(self, doc: Document) -> Document:
        pass

    @property
    def current_params_values(self):
        return self._current_params_values

    # todo: this code requires testing later.
    @current_params_values.setter
    def current_params_values(self, params: dict[str, object]):
        # checking if the parameters and the type of its values are correct
        for param, value in params:
            if param not in self.INITIAL_PARAMS_VALUES.keys():
                raise KeyError(f"{param} is not a parameter for this processor")

            elif not isinstance(value, type(self.INITIAL_PARAMS_VALUES[param])):
                raise TypeError(f"{value} is not suitable for {param}," +
                                f"\n {param} only takes values of type" +
                                f" {type(self.INITIAL_PARAMS_VALUES[param])}")

        # assigning the values of all parameters from the given or default
        # values
        for param in self.INITIAL_PARAMS_VALUES.keys():
            self._current_params_values[param] =\
                params.get(param, self.INITIAL_PARAMS_VALUES[param])
