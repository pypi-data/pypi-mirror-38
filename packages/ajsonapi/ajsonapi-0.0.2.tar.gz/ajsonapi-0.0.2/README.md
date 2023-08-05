# ajsonapi: asynchronous JSON API


## What is it?

*ajsonapi* is a Python package providing the creation of a [JSON
API][json-api] web server backed by a database from a user-provided object
model.


## How to specify an object model?

Let's look at a simple object model specification.

```python
  from ajsonapi import (JSON_API,
                        OneToManyRelationship,
                        ManyToOneRelationship,
                        Attribute,
                        String)

  class Persons(JSON_API):
      name = Attribute(String)
      articles = OneToManyRelationship('Articles', rfkey='person_id')

  class Articles(JSON_API):
      title = Attribute(String)
      author = ManyToOneRelationship('Persons', lfkey='person_id')
```

This model contains two class definitions: `Persons` and `Articles`. A person
has a name and can author zero of more articles. An article has a title and
has exactly one author (who is a person). The only parts in the model that may
be unobvious are the `lfkey` and `rfkey` parameters in the relationship
definitions. They are abbreviations for *local foreign key* and *remote
foreign key*, respectively. Ajsonapi uses these parameters to identify that
`Persons.articles` and `Articles.author` are each other's reverse relationship
and to persist objects and their relationships in the database.

For a more elaborate (albeit abstract) object model see [ajsonapi's model for
functional testing][functest-model].


## What does ajsonapi provide?

From the above six line model, ajsonapi creates a web server that supports the
following twenty-one operations (combinations of HTTP method and URI) as
described by the [JSON API specification][json-api-spec].

```
  GET, POST                 /persons
  GET, PATCH, DELETE        /persons/{id}
  GET, POST, PATCH, DELETE  /persons/{id}/relationships/articles
  GET, POST                 /persons/{id}/articles
  GET, POST                 /articles
  GET, PATCH, DELETE        /articles/{id}
  GET, PATCH                /articles/{id}/relationships/author
  GET, PATCH, DELETE        /articles/{id}/author
```

All objects created and manipulated through the web server are persisted in a
Postgres database by ajsonapi.


## Verion 0.0.2

Note that ajsonapi is work in progress and as of version 0.0.2 only supports
the following ten operations. Furthermore, relationships specified in the JSON
documents accompanying the POST and PATCH requests are ignored.

```
  GET, POST                 /persons
  GET, PATCH, DELETE        /persons/{id}
  GET, POST                 /articles
  GET, PATCH, DELETE        /articles/{id}
```


## Where to get it?

```sh
  pip install ajsonapi
```



[json-api]: https://jsonapi.org
[json-api-spec]: https://jsonapi.org/format
[functest-model]: https://gitlab.com/rvdg/aiojsonapi/aiojsonapi/functests/model.py
