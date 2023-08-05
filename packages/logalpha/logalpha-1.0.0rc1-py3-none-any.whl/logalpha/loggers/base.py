# This file is part of the LogAlpha package.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""
"""

# standard libs
from numbers import Number
from typing import List, Union
from itertools import zip_longest

# internal libs
from ..handlers.base import BaseHandler


class BaseLogger:
    """
    Relays logging messages to all member handlers.
    """

    def __init__(self, handlers: List[BaseHandler]=[], level: str=None) -> None:
        """
        Initialize list of member handlers.
        """
        self.__handlers = list()
        for handler in handlers:
            self.add_handler(handler)

        if handlers and level is not None:
            self.levels = level

    @property
    def handlers(self) -> List[BaseHandler]:
        """Access to member handlers."""
        return self.__handlers

    def add_handler(self, handler: BaseHandler) -> None:
        """Add a handler to list of members."""
        if not isinstance(handler, BaseHandler):
            raise TypeError(f'{self.__class__.__qualname__}.add_handler expects {BaseHandler}, '
                            f'given {type(handler)}.')
        else:
            self.__handlers.append(handler)

    def write(self, *args, **kwargs) -> None:
        """Relays call to all handlers."""
        for handler in self.handlers:
            handler.write(*args, **kwargs)

    def debug(self, message: str, *args, **kwargs) -> None:
        """Calls write() with level='debug'."""
        self.write(message, *args, level='DEBUG', **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        """Calls write() with level='info'."""
        self.write(message, *args, level='INFO', **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        """Calls write() with level='warning'."""
        self.write(message, *args, level='WARNING', **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        """Calls write() with level='error'."""
        self.write(message, *args, level='ERROR', **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        """Calls write() with level='critical'."""
        self.write(message, *args, level='CRITICAL', **kwargs)

    def __str__(self) -> str:
        """String representation of BaseLogger."""
        class_name = self.__class__.__name__
        left_spacing = ' ' * (len(class_name) + 2)
        handler_reprs = f',\n{left_spacing}'.join([str(handler) for handler in self.handlers])
        return f'{class_name}([{handler_reprs}])'

    def __repr__(self) -> str:
        """String representation of BaseLogger."""
        return str(self)

    @property
    def levels(self) -> List[str]:
        """Logging levels for handlers."""
        return [handler.level for handler in self.handlers]

    @levels.setter
    def levels(self, other: Union[str, List[str], Number, List[Number]]) -> None:
        """Validate and assign logging level for this handler."""
        if len(self.handlers) < 1:
            raise AttributeError(f'Cannot set {self.__class__.__qualname__}.levels when '
                                 f'there are no handlers.')
        if isinstance(other, str) or not hasattr(other, '__iter__'):
            for value, handler in zip_longest([other], self.handlers, fillvalue=other):
                handler.level = value
        else:
            if len(other) == len(self.handlers):
                for value, handler in zip(other, self.handlers):
                    handler.level = value
            else:
                raise ValueError(f'{self.__class__.__qualname__}.levels expects the same number '
                                 f'of values as it has handlers.')
