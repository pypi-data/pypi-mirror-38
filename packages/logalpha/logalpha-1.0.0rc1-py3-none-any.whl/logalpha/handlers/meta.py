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

ANSI_RESET = '\033[0m'
ANSI_COLORS = {prefix: {color: '\033[{prefix}{num}m'.format(prefix=i + 3, num=j)
                        for j, color in enumerate(['black', 'red', 'green', 'yellow', 'blue',
                                                   'magenta', 'cyan', 'white'])}
               for i, prefix in enumerate(['foreground', 'background'])}

LOG_COLORS = {'DEBUG': 'blue', 'INFO': 'green', 'WARNING': 'yellow',
              'ERROR': 'red', 'CRITICAL': 'magenta'}

LOG_LEVELS = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 4, 'CRITICAL': 5}
LOG_VALUES = dict((v, k) for k, v in LOG_LEVELS.items())
