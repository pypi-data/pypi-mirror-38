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
"""Module table provides class Table."""

from asyncio import create_task, wait
from itertools import chain

from toposort import toposort

from ajsonapi.attribute import Attribute
from ajsonapi.conversions import pascal_to_snake
# pylint: disable=unused-import
from ajsonapi.relationships import (LocalRelationship, ManyToManyRelationship,
                                    ManyToOneRelationship, Relationship)


class Table:
    """Class Table is the Python representation of an SQL table."""

    by_name = {}

    @classmethod
    def __init_subclass__(cls):
        # pylint: disable=too-many-branches
        if cls.__name__ == 'JSON_API':
            return
        cls.name = pascal_to_snake(cls.__name__)
        cls.id = None
        cls.attributes = []
        cls.relationships = []
        cls.local_relationships = []
        cls.columns = []
        cls.constraints = []
        cls.pool = None

        # Update relationships to class 'cls' for classes in cls.by_name.
        for table in Table.by_name.values():
            for col in table.__dict__.values():
                if isinstance(col, Relationship):
                    if col.rtable == cls.__name__:
                        col.rtable = cls
                    if isinstance(col, ManyToManyRelationship):
                        if col.atable == cls.__name__:
                            col.atable = cls

        # Now insert cls in by_name in case it contains a relationship to
        # itself. That way the next code section resolves the circular
        # dependency.
        Table.by_name[cls.__name__] = cls

        # Update attributes and relationships in cls.
        for name, col in cls.__dict__.items():
            if isinstance(col, Attribute):
                cls.columns.append(col)
                cls.attributes.append(col)
                col.name = name
            elif isinstance(col, Relationship):
                cls.relationships.append(col)
                if isinstance(col, LocalRelationship):
                    cls.local_relationships.append(col)
                    cls.columns.append(col)
                    cls.constraints.append(col)
                col.name = name
                col.lclass = cls
                if (isinstance(col.rtable, str) and
                        col.rtable in Table.by_name):
                    col.rtable = Table.by_name[col.rtable]
                    for rel in col.rtable.relationships:
                        if col.is_reverse(rel):
                            rel.reverse = col
                            col.reverse = rel
                if (isinstance(col, ManyToManyRelationship) and
                        isinstance(col.atable, str)):
                    if col.atable in Table.by_name:
                        col.atable = Table.by_name[col.atable]
                    else:
                        ltablename = cls.__name__
                        if isinstance(col.rtable, str):
                            rtablename = col.rtable
                        else:
                            rtablename = col.rtable.__name__
                        cls_def = (f"class {col.atable}(Table):\n"
                                   f"    rel0 = ManyToOneRelationship"
                                   f"('{ltablename}', lfkey='{col.lafkey}')\n"
                                   f"    rel1 = ManyToOneRelationship"
                                   f"('{rtablename}', lfkey='{col.rafkey}')\n")
                        # pylint: disable=exec-used
                        exec(compile(cls_def, '<string>', 'exec'))

    @classmethod
    async def create(cls):
        """Creates the SQL table, which represents this association table
        class.

        Args:
            pool: Connection pool to the database in which to create the SQL
                tables for this class of the object model.
        """
        table_fields = ',\n    '.join(
            chain((col.sql() for col in cls.columns),
                  (col.sql_constraint() for col in cls.constraints)))
        stmt = (f'CREATE TABLE {cls.__name__} (\n'
                f'    {table_fields}\n'
                f');\n')
        async with cls.pool.acquire() as connection:
            await connection.execute(stmt)

    @classmethod
    async def select(cls, *columns, where=None):
        """Executes an SQL select statement."""

        if where:
            stmt = (f"SELECT {', '.join(col.name for col in columns)}\n"
                    f"FROM {cls.__name__}\n"
                    f"WHERE {where};\n")
        else:
            stmt = (f"SELECT {', '.join(col.name for col in columns)}\n"
                    f"FROM {cls.__name__};\n")
        async with cls.pool.acquire() as connection:
            return await connection.fetch(stmt)

    @classmethod
    async def delete(cls, where):
        """Executes an SQL delete statement."""

        stmt = f'DELETE FROM {cls.__name__} WHERE {where};\n'
        async with cls.pool.acquire() as connection:
            return await connection.execute(stmt)

    @classmethod
    async def update(cls, *, where=None, **kwargs):
        """Executes an SQL update statement."""

        assignments = ', '.join(
            f'{col_name} = {value!r}' for col_name, value in kwargs.items())
        if where:
            stmt = f'UPDATE {cls.name} SET {assignments} WHERE {where};\n'
        else:
            stmt = f'UPDATE {cls.name} SET {assignments};\n'
        async with cls.pool.acquire() as connection:
            return await connection.execute(stmt)

    @classmethod
    def dependencies(cls):
        """Fetches the creation dependencies for this class.

        Returns:
            A set of classes whose tables must be created before this class's
            table.
        """
        return {rel.rtable for rel in cls.local_relationships}


async def create_all():
    """Creates the SQL tables for the classes in the object model.

    Args:
        pool: Connection pool of the database in which to create the SQL
            tables for this obejct model.
    """

    dependencies = {
        table: table.dependencies() for table in Table.by_name.values()
    }
    for tables in toposort(dependencies):
        tasks = {create_task(table.create()) for table in tables}
        await wait(tasks)


def init(pool):
    """Initializes all user Table subclasses."""

    for table in Table.__subclasses__():
        if table.__name__ != 'JSON_API':
            table.pool = pool
