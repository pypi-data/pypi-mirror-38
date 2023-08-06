# Copyright (C) 2018 Rustam Sayfutdinov, rstm.sf@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from kmqc import api
from kmqc import base
from kmqc import config
from kmqc import gates
from kmqc import program

from kmqc.api import Connection
from kmqc.base import Qubit
from kmqc.config import config
from kmqc.gates import DEFINITE_GATES
from kmqc.program import Program


__all__ = [
    'connect', 'Connection',
    'Qubit'
    'config'
    'DEFINITE_GATES',
    'Program',
]

__version__ = '1.0.1.0'


def connect(*args, **kwargs):
    return Connection(*args, **kwargs)


connect.__doc__ = Connection.__init__.__doc__
