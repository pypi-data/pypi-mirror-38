from __future__ import absolute_import

import yaml.loader


class Loader(yaml.loader.SafeLoader):
    '''
    A JSON/YAML loader that implements the JSON Reference internet draft.

    _See also_, JSON Reference, Internet Draft,
    https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03
    '''
    def __init__(self, ctx):
        stream = ctx.open_uri(ctx.base_uri)
        try:
            super(Loader, self).__init__(stream)
        except:
            stream.close()
            raise

        self.context = ctx

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.dispose()
        self.stream.close()

    def construct_mapping(self, node, deep=True):
        mapping = {}
        mapping.update(
            super(Loader, self).construct_mapping(node, deep=True))

        # JSON Reference
        reference = mapping.get('$ref', None)
        if isinstance(reference, str):
            return self.context.parse_reference(reference)

        return mapping


# Override SafeLoader.construct_yaml_map, given it expects construct_mapping()
# to return a map, and this assumption is broken by the use of references.
Loader.add_constructor(
    'tag:yaml.org,2002:map', Loader.construct_mapping)
