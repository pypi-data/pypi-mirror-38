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
"""Module collection provides class Collection."""

from itertools import chain

from asyncpg.exceptions import UniqueViolationError

from ajsonapi.conversions import id_number_to_name, pascal_to_snake, row_to_data
from ajsonapi.errors import DocumentDataDuplicateIdError, ResourceNotFoundError
from ajsonapi.exceptions import ErrorsException
from ajsonapi.json_api import JSON_API
from ajsonapi.responses import document_response, no_data_response
from ajsonapi.verifiers import verify_data_resource_object


class Collection:
    """Class collection represents a resource collection."""
    # pylint: disable=too-few-public-methods

    by_name = {}

    def __init__(self, name, json_api):
        self.name = name
        self.table = json_api
        self.pool = json_api.pool

    async def get(self, query):
        """Produces the response for a GET /{collection} request."""

        links = {'self': self.path()}
        return document_response(await self.to_document(
            query=query, links=links))

    async def post(self, data, query):
        """Produces the response for a POST /{collection} request."""
        # pylint: disable=unused-argument

        # Verify
        id_number, attributes, _ = verify_data_resource_object(
            data, self.name, None,
            [attr.name for attr in self.table.attributes],
            [rel.name for rel in self.table.relationships])

        # Execute
        try:
            if id_number:
                column_names = ', '.join(chain(['id'], attributes.keys()))
                column_values = ', '.join([
                    repr(val) for val in chain([id_number], attributes.values())
                ])
                stmt = (f"INSERT INTO {self.table.__name__} ({column_names})\n"
                        f"VALUES ({column_values});")
                async with self.pool.acquire() as connection:
                    await connection.execute(stmt)
                return no_data_response()
            column_names = ', '.join(attributes.keys())
            column_values = ', '.join(
                [repr(val) for val in attributes.values()])
            stmt = (f"INSERT INTO {self.table.__name__} ({column_names})\n"
                    f"VALUES ({column_values}) RETURNING id;")
            async with self.pool.acquire() as connection:
                collection_id_number = await connection.fetchval(stmt)
            collection_id_name = id_number_to_name(collection_id_number)
            data = {'type': self.name, 'id': collection_id_name}
            if attributes:
                data['attributes'] = attributes
            path = f'{self.path()}/{collection_id_name}'
            data['links'] = {'self': path}
            return document_response({
                'data': data,
            },
                                     status=201,
                                     headers={'Location': path})
        except UniqueViolationError:
            raise ErrorsException(
                [DocumentDataDuplicateIdError(f"/data/id/{data['id']}")])

    async def to_document(self, query=None, links=None):
        """Creates the document for the resource objects in this resource
        collection.

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
        # pylint: disable=no-self-use,unused-argument

        columns = chain([self.table.id], self.table.attributes)
        results = await self.table.select(*columns)
        return [row_to_data(row, self.name) for row in results], None

    def path(self):
        """Creates the path to the collection."""

        return f'/{self.name}'


def init():
    """Initializes the Collection module."""

    for json_api in JSON_API.__subclasses__():
        collection_name = pascal_to_snake(json_api.__name__)
        Collection.by_name[collection_name] = Collection(
            collection_name, json_api)


def parse_collection(request):
    """Gets a collection associated with a request.

    Args:
        request: Incoming Http(s) request.

    Exceptions:
        ErrorsException: Exception containing a 'resource not found' error.
    """

    collection_name = request.match_info['collection']
    try:
        return Collection.by_name[collection_name]
    except KeyError:
        raise ErrorsException([ResourceNotFoundError(f'/{collection_name}')])
