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

import re
import inspect
from numbers import Number
from typing import Dict, Union
from collections import defaultdict

from .._types import CallbackType, ResourceType
from .meta import (LOG_LEVELS, LOG_VALUES, LOG_COLORS,
                   ANSI_COLORS, ANSI_RESET)


class BaseHandler:
    """
    Base handler for redirecting logging messages.
    """

    default_labels = ('message', 'level', 'LEVEL', 'num')

    def __init__(self, level: str='INFO', template: str='{level} {message}',
                 **callbacks: CallbackType) -> None:
        """
        Initialize attributes, resource, callbacks.
        """

        self.__resource = None  # CallbackType
        self.__counts = defaultdict(lambda: 0)

        self.callbacks = callbacks  # must come before self.template initialization
        self.template = template
        self.level = level

    @property
    def resource(self) -> ResourceType:
        """Access underlying resource (e.g., file object or database connection)."""
        return self.__resource

    @resource.setter
    def resource(self, other: ResourceType) -> None:
        """Validate and assign underlying resource."""

        if isinstance(other, str):
            self.__resource = open(other, mode='a')

        elif not all(hasattr(other, attr) for attr in ('__enter__', '__exit__', 'close')):
            raise TypeError(f'{self.__class__.__qualname__}.resource is expected to be a '
                            f'file-like or connection-like object (e.g., has \"__enter__\"), '
                            f'given, {type(other)}.')
        else:
            self.__resource = other

    @property
    def template(self) -> str:
        """Template defining the logging statement format."""
        return self.__template

    @template.setter
    def template(self, other: str) -> None:
        """Assign new value to template."""

        if not isinstance(other, str):
            raise TypeError(f'{self.__class__.__qualname__}.template should be {str}.')

        elif '{message}' not in other:
            raise ValueError(f'{self.__class__.__qualname__}.template requires that '
                             '{message} at least be present in the string.')

        else:
            for label, callback in self.callbacks.items():
                format_entry = '{' + label + '}'
                if format_entry not in other:
                    raise ValueError(f'{self.__class__.__qualname__}.template is missing '
                                     f'{format_entry} implied in keyword arguments.')

            for match in re.finditer(r'{(\w*)(:\S*}|})', other):
                label = match.groups()[0]
                format_entry = '{' + label + '}'
                if label not in self.callbacks.keys() and label not in self.default_labels:
                    raise KeyError(f'{self.__class__.__qualname__}.template contains '
                                   f'{format_entry} but \"{label}\" was provided as a callback (kwarg).')

            self.__template = other

    @property
    def callbacks(self) -> Dict[str, CallbackType]:
        """Access callbacks (usually, lambda functions)."""
        return self.__callbacks

    @callbacks.setter
    def callbacks(self, other: Dict[str, CallbackType]) -> None:
        """Validate and assign callbacks dictionary."""
        if not isinstance(other, dict):
            raise TypeError(f'{self.__class__.__qualname__}.callbacks should be {dict}, '
                            f'given {type(other)}')

        for key in other.keys():
            if not isinstance(key, str):
                raise TypeError(f'{self.__class__.__qualname__}.callbacks requires all keys to '
                                f'be string-like, found {key} -> {type(key)}')

        for label, callback in other.items():
            if not hasattr(callback, '__call__'):
                raise TypeError(f'{self.__class__.__qualname__}.callbacks requires all values be '
                                f'callable, {label} has no attribute \"__call__\".')

        for label, callback in other.items():
            if not len(inspect.signature(callback).parameters) == 0:
                raise ValueError(f'{self.__class__.__qualname__}.callbacks requires all callables/functions have '
                                 f'zero parameters, found {label}{inspect.signature(callback)}.')
        else:
            self.__callbacks = other

    @property
    def level(self) -> str:
        """Logging level for handlers."""
        return self.__level

    @level.setter
    def level(self, other: Union[str, Number]) -> None:
        """Validate and assign logging level for this handler."""
        if isinstance(other, str):
            if other.upper() not in LOG_LEVELS.keys():
                raise ValueError(f'{self.__class__.__qualname__}.level expects one of '
                                 f'{tuple(LOG_LEVELS.keys())}')
            else:
                self.__level = other.upper()

        elif isinstance(other, Number):
            if int(other) not in LOG_LEVELS.values():
                raise ValueError(f'{self.__class__.__qualname__}.level accepts integers between 0-5'
                                 f', given {other}.')
            else:
                self.__level = LOG_VALUES[int(other)]

        else:
            raise TypeError(f'{self.__class__.__qualname__}.level requires either a string-like or '
                            f'number-like value, given {type(other)}.')

    @property
    def counts(self) -> Dict[str, int]:
        """Counter of number of times each level has been written to."""
        return self.__counts

    def __del__(self) -> None:
        """Release "resource"."""
        if hasattr(self.resource, 'close'):
            self.resource.close()

    def write(self, message: str, level: str, colorize: bool=False) -> None:
        """Filters out messages based on 'level' and sends to target resource."""

        # check valid level assignment
        if level.upper() not in LOG_LEVELS:
            raise ValueError(f'{self.__class__.__qualname__}.level expects one of '
                             f'{tuple(LOG_LEVELS.keys())}')

        # increment call count
        self.counts[level.upper()] += 1

        # only proceed if level is sufficient
        if LOG_LEVELS[level.upper()] < LOG_LEVELS[self.level]:
            return

        # initial construction has no formatting
        callback_results = {label: str(callback()) for label, callback in self.callbacks.items()}

        if '{level}' in self.template:
            callback_results['level'] = level.lower()

        if '{LEVEL}' in self.template:
            callback_results['LEVEL'] = level.upper()

        if '{num}' in self.template:
            callback_results['num'] = str(self.counts[level.upper()])

        if colorize is True:
            ANSI_CODE = ANSI_COLORS['foreground'][LOG_COLORS[level.upper()]]
            callback_results = {label: ANSI_CODE + value + ANSI_RESET
                                for label, value in callback_results.items()}

        message = self.template.format(**{'message': message, **callback_results})
        message = message.strip('\n') + '\n'
        self._write(message)

    def _write(self, message: str) -> None:
        """Flush prepared/formatted string 'message' to resource."""
        self.resource.write(message)
        self.resource.flush()

    def __str__(self) -> str:
        """String representation of handler."""
        return (f'{self.__class__.__name__}(template=\'{self.template}\', '
                f'level=\'{self.level}\')')

    def __repr__(self) -> str:
        """String representation of handler."""
        return str(self)
