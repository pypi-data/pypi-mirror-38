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
from io import TextIOWrapper
from typing import Union

# internal libs
from .base import BaseHandler


class FileHandler(BaseHandler):
    """
    Handles logging messages targeting a file-like object.
    """

    def __init__(self, *args, file: Union[str, TextIOWrapper], **kwargs) -> None:
        """
        See Also:
        BaseHandler.__init__()
            For full signature and descriptions.
        """
        super().__init__(*args, **kwargs)
        self.resource = file
