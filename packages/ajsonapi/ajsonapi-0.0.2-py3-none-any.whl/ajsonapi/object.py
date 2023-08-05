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
"""Module object provides class Object."""

from itertools import chain

from ajsonapi.conversions import id_name_to_number, row_to_data
from ajsonapi.errors import (ResourceNotFoundError,
                             ResourceNotFoundMalformedIdError)
from ajsonapi.exceptions import ErrorsException
from ajsonapi.json_api import JSON_API
from ajsonapi.responses import document_response, no_data_response
from ajsonapi.verifiers import verify_data_resource_object


class Object:
    """Class object represents a resource object."""

    def __init__(self, collection_name, id_name):
        self.collection_name = collection_name
        self.id_name = id_name
        self.table = JSON_API.by_collection_name[collection_name]
        self.pool = self.table.pool
        try:
            self.id_number = id_name_to_number(id_name)
        except ValueError:
            raise ErrorsException([
                ResourceNotFoundMalformedIdError(
                    f'/{collection_name}/{id_name}')
            ])

    async def get(self, query):
        """Produces the response for a GET /{collection}/{id} request."""

        links = {'self': self.path()}
        return document_response(await self.to_document(
            query=query, links=links))

    async def delete(self):
        """Removes the object from the database and produces the response for
        a DELETE /{collection}/{id} request.
        """

        where = f'id = {self.id_number!r}'
        result = await self.table.delete(where=where)
        if result == 'DELETE 0':
            raise ErrorsException([ResourceNotFoundError(self.path())])
        return no_data_response()

    async def patch(self, data, query):
        """Patches the object in the database and produces the response for a
        PATCH /{collection}/{id} request.
        """

        id_number, attributes, relationships = verify_data_resource_object(
            data, self.table.name, self.id_name,
            [attr.name for attr in self.table.attributes],
            [rel.name for rel in self.table.relationships])
        if attributes or relationships:
            where = f'id = {id_number!r}'
            result = await self.table.update(**attributes, where=where)
            if result == 'UPDATE 0':
                raise ErrorsException([ResourceNotFoundError(self.path())])
        links = {'self': self.path()}
        return document_response(await self.to_document(
            query=query, links=links))

    async def to_document(self, query=None, links=None):
        """Creates the document for this resource object.

        Args:
            links (dict): value for the links field in the response.
        """

        data, _ = await self.to_data_included(query)
        document = {'data': data}
        if links:
            document['links'] = links
        return document

    async def to_data_included(self, query):
        """Creates the response document's data and included member values."""
        # pylint: disable=unused-argument

        columns = chain([self.table.id], self.table.attributes)
        where = f"id = {self.id_number!r}"
        results = await self.table.select(*columns, where=where)
        if not results:
            raise ErrorsException([ResourceNotFoundError(self.path())])
        return row_to_data(results[0], self.collection_name), None

    def path(self):
        """Creates the path to the collection."""

        return f'/{self.collection_name}/{self.id_name}'


def parse(request):
    """Gets an object associated with the request.

    Args:
        request: Incoming Http(s) request.

    Exceptions:
        ErrorsException: Exception containing a 'resource not found' error.
    """
    # pylint: disable=unused-argument

    collection_name = request.match_info['collection']
    id_name = request.match_info['id']
    try:
        return Object(collection_name, id_name)
    except KeyError:
        raise ErrorsException([ResourceNotFoundError(f'/{collection_name}')])
