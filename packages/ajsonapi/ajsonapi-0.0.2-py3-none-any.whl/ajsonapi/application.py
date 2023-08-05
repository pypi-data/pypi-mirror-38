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
"""Module application provides class Application."""

from aiohttp import web
from asyncpg.pool import create_pool

from ajsonapi.exceptions import ErrorsException
from ajsonapi.init import init
from ajsonapi.requests import (parse_collection_document_query,
                               parse_collection_query,
                               parse_object_document_query, parse_object_query)
from ajsonapi.responses import errors_response
from ajsonapi.table import create_all as table_create_all


class Application:
    """JSON API web server.

    Default routes are derived from the specified object model.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, *args, **kwargs):
        self.app = web.Application(*args, **kwargs)
        self.pool = None

    async def connect_database(self, database):
        """Connects to the database."""
        self.pool = await create_pool(database)
        init(self.pool)

    async def disconnect_database(self):
        """Disconnects from the database."""
        await self.pool.close()

    async def create_tables(self):
        """Creates all tables in the database."""
        await table_create_all()

    def add_json_api_routes(self):
        """Add JSON API routes to the web application."""
        path = r'/{collection:[^/]*}'
        self.app.router.add_get(path, self.get_collection)
        self.app.router.add_post(path, self.post_collection)

        path = r'/{collection:[^/]*}/{id:[0-9A-Fa-f-]*}'
        self.app.router.add_get(path, self.get_object)
        self.app.router.add_delete(path, self.delete_object)
        self.app.router.add_patch(path, self.patch_object)

    async def get_collection(self, request):
        """Entry point for GET /{collection} requests.

        Args:
            request: The GET /{collection} request.
        """

        try:
            collection, query = parse_collection_query(request)
            return await collection.get(query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def post_collection(self, request):
        """Entry point for GET /{collection} requests.

        Args:
            request: The POST /{collection} request.
        """

        try:
            collection, data, query = await parse_collection_document_query(
                request)
            return await collection.post(data, query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def get_object(self, request):
        """Entry point for GET /{collection}/{id} requests.

        Args:
            request: The GET /{collection}/{id} request.
        """
        try:
            object_, query = await parse_object_query(request)
            return await object_.get(query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def delete_object(self, request):
        """Entry point for DELETE /{collection}/{id} requests.

        Args:
            request: The DELETE /{collection}/{id} request.
        """
        try:
            object_, _ = await parse_object_query(request)
            return await object_.delete()
        except ErrorsException as err:
            return errors_response(err.errors)

    async def patch_object(self, request):
        """Entry point for DELETE /{collection}/{id} requests.

        Args:
            request: The DELETE /{collection}/{id} request.
        """
        try:
            object_, data, query = await parse_object_document_query(request)
            return await object_.patch(data, query)
        except ErrorsException as err:
            return errors_response(err.errors)
