# Copyright (c) 2018 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
ajsonapi - asynchronous JSON API
================================

**ajsonapi** is a Python package providing the creation of a JSON API web
server backed by a database from a user-provided object model.
"""

from sys import version_info
assert version_info >= (3, 7), 'Need Python 3.7+ for module ajsonapi'
del version_info

__docformat__ = 'restructuredtext'
__version__ = '0.0.3'

from ajsonapi.application import Application
from ajsonapi.attribute import Attribute
from ajsonapi.json_api import JSON_API
from ajsonapi.relationships import ManyToManyRelationship
from ajsonapi.relationships import ManyToOneRelationship
from ajsonapi.relationships import OneToManyRelationship
from ajsonapi.relationships import OneToOneLocalRelationship
from ajsonapi.relationships import OneToOneRemoteRelationship
from ajsonapi.types import Int64
from ajsonapi.types import String
