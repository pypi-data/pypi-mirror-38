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
import sys

# internal libs
from .base import BaseHandler


class ConsoleHandler(BaseHandler):
    """
    Handles logging messages targeting <stdout/stderr>.
    """

    default_stream = {'DEBUG':    sys.stdout,
                      'INFO':     sys.stdout,
                      'WARNING':  sys.stderr,
                      'ERROR':    sys.stderr,
                      'CRITICAL': sys.stderr}

    def __init__(self, *args, colorize: bool=True,
                 stderr_only: bool=False, **kwargs) -> None:
        """
        See Also:
        Handler.__init__()
            For full signature and descriptions.
        """
        super().__init__(*args, **kwargs)
        self.colorize = colorize
        if stderr_only is True:
            self.default_stream.update({'DEBUG': sys.stderr,
                                        'INFO': sys.stderr})

    def write(self, *args, level: str, **kwargs) -> None:
        """Writes to <stdout> for DEBUG/INFO, <stderr> otherwise."""
        self.resource = self.default_stream[level.upper()]
        super().write(*args, level=level, colorize=self.colorize, **kwargs)
