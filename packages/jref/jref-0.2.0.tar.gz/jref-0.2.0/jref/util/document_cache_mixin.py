__metaclass__ = type

_DOCUMENT_CACHE = {}


def _cache_key(ctx):
    key = ()

    if ctx.DOCUMENT_CACHE_ATTRIBUTE:
        key += (getattr(ctx, ctx.DOCUMENT_CACHE_ATTRIBUTE),)

    uri = ctx.base_uri
    key += (type(uri), uri)

    return key


class DocumentCacheMixin:
    DOCUMENT_CACHE_ATTRIBUTE = None

    def load_document(self):
        key = _cache_key(self)
        try:
            return _DOCUMENT_CACHE[key]
        except KeyError:
            pass

        doc = super(DocumentCacheMixin, self).load_document()
        _DOCUMENT_CACHE[key] = doc

        return doc
