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
LogAlpha
========

A minimalist yet robust approach to logging in Python.
LogAlpha handles the rather basic task of filtering, formatting,
and colorizing metadata alongside messages.

Example
-------
    >>> import logalpha as logging
    >>> log = logging.getlogger('example')
    >>> log.info('test')
    info 08:47:32 example: test
"""

from .handlers import ConsoleHandler, FileHandler
from .loggers import BaseLogger
