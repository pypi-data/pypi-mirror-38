# Copyright (c) 2015-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from __future__ import absolute_import
import re
from .__about__ import __version__
__version__ = re.sub(r"(\.0)+$", "", __version__)
del re, absolute_import
