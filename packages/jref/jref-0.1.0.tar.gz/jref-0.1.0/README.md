# python-jref

This python package implements the JSON Reference and JSON Pointer
specifications in the context of processing JSON and YAML content, such as
Swagger and OpenAPI specifications.

## JSON Reference

JSON Reference defines a mechanism to reference and include content from the
same or separate documents. This helps with maintenance of structured data and
documents by reducing repetition, and allowing for the organization of larger
documents across multiple files.

## JSON Pointer

JSON Pointer defines a syntax for identifying specific portions of a JSON
value.

In a document, a JSON Reference takes the form of an object, mapping '$ref' to a
reference; other keys in the object are ignored. The reference itself takes the
form of a URI. As an example:

    { "$ref": "http://example.com/example.json#/foo/bar" }

In this implementation, the URI may reference a JSON or YAML file available in
the local filesystem, or served from the network over HTTP/HTTPS. The fragment
portion of the URI is interpreted as a JSON Pointer.

## Usage example

Find the example below also as [`usage-example.py`](usage-example.py) in the
source repository.

```python
import os
import textwrap

import jref.context
import jref.pointer

# All references are evaluated in a context, so start with one
ctx = jref.context.RemoteContext()

# Reference a remote document
spec = ctx.parse_reference('https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml')

# Reference portions of that document
spec_title = spec.context.parse_reference('#/info/title')
spec_version = spec.context.parse_reference('#/info/version')

# Print out the references, not the content (which hasn't been loaded)
print(textwrap.dedent('''
    * JSON References
    Spec:    {}
    Title:   {}
    Version: {}
    ''')
    .lstrip()
    .format(spec, spec_title, spec_version))

# Expand references, triggering loading of content
print(textwrap.dedent('''
    * Evaluated references
    Title:   {}
    Version: {}
    ''')
    .lstrip()
    .format(spec_title.expand(), spec_version.expand()))
```

Expected output:

```
* JSON References
Spec:    https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml
Title:   https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml#/info/title
Version: https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml#/info/version

* Evaluated references
Title:   Swagger Petstore
Version: 1.0.0

```

## References

* JSON Reference, Internet Draft,
  https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03
* JSON Pointer, RFC 6901, https://tools.ietf.org/html/rfc6901
