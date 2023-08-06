'''
Contexts control the resolution of URIs, and provide a way to limit access to
the local filesystem and to remote resources.
'''
import contextlib
import os

try:
    from urllib.parse import unquote, urljoin, urlparse
    from urllib.request import url2pathname
except ImportError:
    # Python 2
    from urlparse import unquote, urljoin, urlparse
    from urllib import url2pathname

import jref.error
import jref.reference
import jref.uri
import jref.util
import jref.yaml


__metaclass__ = type


class ContextError(jref.error.Error):
    pass


class LocalPathOutsideContextRoot(ContextError):
    MESSAGE = 'Local path points outside context root, \'{1}\': {0}'


class NoLocalPathInContext(ContextError):
    MESSAGE = 'Local path is not allowed in this context: {0}'


class NoRemoteURIInContext(ContextError):
    MESSAGE = 'Remote URI is not allowed in this context: {0}'


class NoAbsolutePathInContext(ContextError):
    MESSAGE = 'Absolute path is not allowed in this context: {0}'


class ProtocolMissingInRemoteURI(ContextError):
    MESSAGE = 'Missing protocol in remote URI: {0}'


class ProtocolNotSupportedInContext(ContextError):
    MESSAGE = 'Unsupported protocol in URI: {0}'


def _scheme_from_uri(uri):
    for i, ch in enumerate(uri):
        if ch == '/':
            return None
        if ch == ':':
            return uri[:i].lower()

    return None


class BaseContext:
    DEFAULT_URI = ''
    PATH_SEPARATOR = '/'

    def __init__(self, base_uri=None):
        if base_uri is None:
            base_uri = self.DEFAULT_URI

        if type(base_uri) is type(''):
            base_uri = self.normalize_uri(base_uri)

        self.base_uri = base_uri

    def context_for(self, uri):
        if isinstance(uri, jref.uri.LocalPath):
            return self.context_for_local_path(uri)
        if isinstance(uri, jref.uri.RemoteURI):
            return self.context_for_remote_uri(uri)
        raise NotImplementedError()

    def context_for_local_path(self, path):
        raise NotImplementedError()

    def context_for_remote_uri(self, uri):
        raise NotImplementedError()

    def load_document(self):
        with jref.yaml.Loader(self) as loader:
            return loader.get_single_data()

    def normalize_uri(self, uri):
        scheme = _scheme_from_uri(uri)
        if scheme == 'file':
            path = url2pathname(uri[len('file:'):])
            return self.normalize_local_path(path)
        if scheme:
            return self.normalize_remote_uri(uri)

        if uri.startswith(self.PATH_SEPARATOR):
            return self.normalize_absolute_path(uri)
        return self.normalize_relative_path(uri)

    def normalize_absolute_path(self, path):
        if isinstance(self.base_uri, jref.uri.RemoteURI):
            return self.normalize_relative_path(path)
        raise NoAbsolutePathInContext(path)

    def normalize_local_path(self, path):
        path = path.replace(self.PATH_SEPARATOR, os.sep)
        return jref.uri.LocalPath(os.path.normpath(path))

    def normalize_relative_path(self, path):
        if isinstance(self.base_uri, jref.uri.RemoteURI):
            return self.normalize_remote_uri(path)
        raise NotImplementedError()

    def normalize_remote_uri(self, uri):
        url = urlparse(uri, allow_fragments=False)
        return jref.uri.RemoteURI(url.geturl())

    def open_uri(self, uri):
        if isinstance(uri, jref.uri.LocalPath):
            return self.open_local_path(uri)
        if isinstance(uri, jref.uri.RemoteURI):
            return self.open_remote_uri(uri)
        raise NotImplementedError()

    @staticmethod
    def open_local_path(path):
        return open(path, 'rb')

    @staticmethod
    def open_remote_uri(uri):
        return jref.util.StreamingRequest(uri)

    def parse_reference(self, ref):
        uri, _, fragment = ref.partition('#')
        if uri:
            uri = self.normalize_uri(uri)
            uri = self.validate(uri)
            ctx = self.context_for(uri)
        else:
            ctx = self

        return jref.reference.Reference(ctx, unquote(fragment))

    def validate(self, uri):
        if isinstance(uri, jref.uri.LocalPath):
            return self.validate_local_path(uri)
        if isinstance(uri, jref.uri.RemoteURI):
            return self.validate_remote_uri(uri)
        raise NotImplementedError()

    def validate_local_path(self, path):
        raise NoLocalPathInContext(path)

    def validate_remote_uri(self, uri):
        raise NoRemoteURIInContext(uri)


class LocalContext(jref.util.DocumentCacheMixin, BaseContext):
    '''A context that can only process local paths. If a base_uri is specified,
    only paths under base_uri will be allowed.
    '''
    DEFAULT_URI = jref.uri.LocalPath()
    DOCUMENT_CACHE_ATTRIBUTE = 'root'

    def __init__(self, base_uri=None, root=''):
        super(LocalContext, self).__init__(base_uri)

        self.root = root
        self.directory = os.path.dirname(self.base_uri)

    def normalize_relative_path(self, path):
        return self.normalize_local_path(path)

    def open_local_path(self, path):
        absolute_path = \
            os.path.abspath(os.path.join(self.root, path))
        return super(LocalContext, self).open_local_path(absolute_path)

    def context_for_local_path(self, path):
        return self.__class__(path, root=self.root)

    def validate_local_path(self, path):
        local_path = self.normalize_local_path(
            os.path.join(self.directory, path))

        if local_path.startswith(os.path.pardir + os.sep):
            raise LocalPathOutsideContextRoot(local_path, self.root)

        return local_path


class RemoteContext(jref.util.DocumentCacheMixin, BaseContext):
    '''A context that can only process remote URIs.'''
    DEFAULT_URI = jref.uri.RemoteURI()

    def context_for_remote_uri(self, uri):
        return RemoteContext(uri)

    def validate_remote_uri(self, uri):
        scheme = _scheme_from_uri(uri)
        if not scheme:
            raise ProtocolMissingInRemoteURI(uri)
        if scheme not in ('http', 'https'):
            raise ProtocolNotSupportedInContext(uri)

        return jref.uri.RemoteURI(urljoin(self.base_uri, uri))


class LocalOrRemoteContext(LocalContext, RemoteContext):
    '''A context that can process remote URIs, along with relative paths in the
    local filesystem.

    Local files get assigned a context of the same class, and may reference
    local files, using relative paths, as well as remote URIs.

    Remote URIs get assigned a RemoteContext and may only reference other remote
    URIs.
    '''


class CLIContext(LocalOrRemoteContext):
    '''A context that can process remote URIs, along with relative and absolute
    paths in the local filesystem.

    Local files get assigned a LocalOrRemoteContext, allowing them to reference
    local files using (ONLY) relative paths, as well as remote URIs.

    Remote URIs get assigned a RemoteContext and may only reference other Remote
    URIs.
    '''
    __class__ = LocalOrRemoteContext

    def normalize_absolute_path(self, path):
        return self.normalize_local_path(path)
