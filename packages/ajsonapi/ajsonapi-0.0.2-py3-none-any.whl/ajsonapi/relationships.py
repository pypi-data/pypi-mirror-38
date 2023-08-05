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
"""Module relationships provides relationship classes."""

from abc import ABC, abstractmethod


class Relationship(ABC):
    """Abstract base class for all relationships between resources.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, rtable):
        self.rtable = rtable
        self.name = None  # Overridden in Table.__init_subclass__
        self.reverse = None  # Overridden in Table.__init_subclass__

    @abstractmethod
    def is_reverse(self, other):
        """Detects whether relationships are each other's reverse.

        Args:
            other: A Relationship instance.

        Returns:
           True if self and other are each other's reverse relationship, False
           otherwise.
        """


class LocalRelationship(Relationship):
    """A relationship with a local foreign key."""

    def __init__(self, rtable, lfkey):
        super().__init__(rtable)
        self.lfkey = lfkey

    @abstractmethod
    def is_reverse(self, other):
        pass

    def sql(self):
        """Produces the SQL column definition for the local foreign key of
        this object.

        Returns:
            A string containing the SQL column definition for the local
            foreign key of this object.
        """

        return f'{self.lfkey} UUID'

    def sql_constraint(self):
        """Produces the SQL foreign key constraint for this object.

        Returns:
            A string containing the SQL foreign key constraint for this
            object.
        """

        return (f'FOREIGN KEY ({self.lfkey}) REFERENCES '
                f'{self.rtable.__name__}(id)')


class OneToOneLocalRelationship(LocalRelationship):
    """A one-to-one relationship between resources with a local foreign key.
    """

    def is_reverse(self, other):
        return (isinstance(other, OneToOneRemoteRelationship) and
                other.rfkey == self.lfkey)


class OneToOneRemoteRelationship(Relationship):
    """A one-to-one relationship between resources with a remote foreign key.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, rtable, rfkey):
        super().__init__(rtable)
        self.rfkey = rfkey

    def is_reverse(self, other):
        return (isinstance(other, OneToOneLocalRelationship) and
                other.lfkey == self.rfkey)


class OneToManyRelationship(Relationship):
    """A one-to-many relationship between resources."""

    # pylint: disable=too-few-public-methods

    def __init__(self, rtable, rfkey):
        super().__init__(rtable)
        self.rfkey = rfkey

    def is_reverse(self, other):
        return (isinstance(other, ManyToOneRelationship) and
                other.lfkey == self.rfkey)


class ManyToOneRelationship(LocalRelationship):
    """A many-to-one relationship between resources."""

    def is_reverse(self, other):
        return (isinstance(other, OneToManyRelationship) and
                other.rfkey == self.lfkey)


class ManyToManyRelationship(Relationship):
    """A many-to-many relationship between resources."""

    # pylint: disable=too-few-public-methods

    def __init__(self, rtable, atable, lafkey, rafkey):
        # pylint: disable=too-many-arguments
        super().__init__(rtable)
        self.atable = atable
        self.lafkey = lafkey
        self.rafkey = rafkey

    def is_reverse(self, other):
        return (isinstance(other, ManyToManyRelationship) and
                other.atable == self.atable and other.lafkey == self.rafkey and
                other.rafkey == self.lafkey)
