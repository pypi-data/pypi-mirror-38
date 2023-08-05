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
"""Module query deals with everything related to query parameters."""

from ajsonapi.errors import QueryParameterUnsupportedError
from ajsonapi.exceptions import ErrorsException


def query_has_parameter(query, name):
    """Checks if a query parameter exists."""
    for parameter in query:
        if parameter.split('[')[0] == name:
            return True
    return False


def parse(request):
    """Checks request's query parameters for errors."""

    errors = []
    query = request.query

    includes = {}
    if query_has_parameter(query, 'include'):
        errors.append(QueryParameterUnsupportedError('include'))
    fields = {}
    if query_has_parameter(query, 'fields'):
        errors.append(QueryParameterUnsupportedError('fields'))
    sort = {}
    if query_has_parameter(query, 'sort'):
        errors.append(QueryParameterUnsupportedError('sort'))
    page = None
    if query_has_parameter(query, 'page'):
        errors.append(QueryParameterUnsupportedError('page'))
    filter_ = lambda x: True
    if query_has_parameter(query, 'filter'):
        errors.append(QueryParameterUnsupportedError('filter'))

    if errors:
        raise ErrorsException(errors)
    return {
        'includes': includes,
        'fields': fields,
        'sort': sort,
        'page': page,
        'filter': filter_,
    }
