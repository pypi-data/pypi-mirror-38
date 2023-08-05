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
"""Module jsonapi/checks deals with checking JSON API requests."""

from ajsonapi.conversions import id_name_to_number, uuid_name_to_number
from ajsonapi.errors import (
    DocumentDataInvalidAttributeError, DocumentDataInvalidIdError,
    DocumentDataInvalidRelationshipError, DocumentDataInvalidTypeError,
    DocumentDataMalformedError, DocumentDataMalformedUuidError,
    DocumentDataMissingIdError, DocumentDataMissingTypeError)
from ajsonapi.exceptions import ErrorsException


def verify_data_resource_object(obj, valid_type_name, valid_id_name,
                                valid_attribute_names,
                                valid_relationship_names):
    """Verifies that the object's type, id and attributes are correct.

    Args:
        obj: object that needs verifying.
        valid_type_name (str): valid type name for object.
        valid_attribute_names (list): valid attribute names for object.
        valid_relationship_names (list): valid relationships names for object.

    Return:
        returns the id number and attributes found in the object.
    """

    # pylint: disable=too-many-branches

    errors = []

    # Type
    try:
        type_name = obj['type']
        if type_name != valid_type_name:
            errors.append(
                DocumentDataInvalidTypeError(f'/data/type/{type_name}'))
    except TypeError:
        raise ErrorsException([DocumentDataMalformedError()])
    except KeyError:
        errors.append(DocumentDataMissingTypeError('/data'))

    # Id
    if 'id' in obj:
        id_name = obj['id']
        try:
            if valid_id_name:
                if id_name != valid_id_name:
                    errors.append(
                        DocumentDataInvalidIdError(f'/data/id/{id_name}'))
                id_number = id_name_to_number(id_name)
            else:
                id_number = uuid_name_to_number(id_name)
        except ValueError:
            errors.append(DocumentDataMalformedUuidError(f'/data/id/{id_name}'))
    else:
        if valid_id_name:
            errors.append(DocumentDataMissingIdError())
        id_number = None

    # Attributes
    attributes = obj.get('attributes', {})
    invalid_attribute_names = set(
        attributes.keys()) - set(valid_attribute_names)
    if invalid_attribute_names:
        errors.extend([
            DocumentDataInvalidAttributeError(
                f'/data/attributes/{attribute_name}')
            for attribute_name in invalid_attribute_names
        ])

    # Relationships
    relationships = obj.get('relationships', {})
    invalid_relationship_names = set(
        relationships.keys()) - set(valid_relationship_names)
    if invalid_relationship_names:
        errors.extend([
            DocumentDataInvalidRelationshipError(
                f'/data/relationships/{relationship_name}')
            for relationship_name in invalid_relationship_names
        ])

    if errors:
        raise ErrorsException(errors)
    return id_number, attributes, relationships
