import io
import requests


class StreamingRequest(io.RawIOBase):
    '''Presents the response of an HTTP request as a byte stream.'''
    def __init__(self, uri):
        req = requests.get(uri, stream=True)
        req.raise_for_status()

        self.request = req
        self.iterator = req.iter_content(None)
        self.leftover = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def readable(self):
        return self.iterator is not None

    def readinto(self, buf):
        try:
            chunk = self.leftover or next(self.iterator)
        except StopIteration:
            return 0

        count = min(len(buf), len(chunk))
        buf[:count], self.leftover = chunk[:count], chunk[count:]
        return count

    def close(self):
        super(StreamingRequest, self).close()

        self.request.close()
        self.iterator = None
