"""Testing utilities"""
import io

from tornado import gen
from tornado.httputil import HTTPHeaders
from tornado.httpclient import AsyncHTTPClient, HTTPError, HTTPRequest, HTTPResponse


class MockAsyncHTTPClient(AsyncHTTPClient.configurable_default()):
    mocks = {}
    records = {}

    def url_key(self, url):
        """cache key is url without query

        to avoid caching things like access tokens
        """
        return url.split('?')[0]

    def fetch_mock(self, request):
        """Fetch a mocked request

        Arguments:
            request (HTTPRequest): the request to fetch
        Returns:
            HTTPResponse constructed from the info stored in the mocks
        Raises:
            HTTPError if the cached response has status >= 400
        """
        mock_data = self.mocks[self.url_key(request.url)]
        code = mock_data.get('code', 200)
        headers = HTTPHeaders(mock_data.get('headers', {}))
        response = HTTPResponse(request, code, headers=headers)
        response.buffer = io.BytesIO(mock_data['body'].encode('utf8'))
        if code >= 400:
            raise HTTPError(mock_data['code'], response=response)

        return response

    def _record_response(self, url_key, response):
        """Record a response in self.records"""
        self.records[url_key] = {
            'code': response.code,
            'headers': dict(response.headers),
            'body': response.body.decode('utf8'),
        }

    async def fetch(self, req_or_url, *args, **kwargs):
        """Mocked HTTP fetch

        If the request URL is in self.mocks, build a response from the cached response.
        Otherwise, run the actual request and store the response in self.records.
        """
        if isinstance(req_or_url, HTTPRequest):
            request = req_or_url
        else:
            request = HTTPRequest(req_or_url, *args, **kwargs)

        url_key = self.url_key(request.url)

        if url_key in self.mocks:
            fetch = self.fetch_mock
        else:
            fetch = super().fetch

        error = None
        try:
            response = await gen.maybe_future(fetch(request))
        except HTTPError as e:
            error = e
            response = e.response

        self._record_response(url_key, response)
        # return or raise the original result
        if error:
            raise error
        else:
            return response


# async-request utility from jupyterhub.tests.utils v0.8.1
# used under BSD license

from concurrent.futures import ThreadPoolExecutor
import requests


class _AsyncRequests:
    """Wrapper around requests to return a Future from request methods

    A single thread is allocated to avoid blocking the IOLoop thread.
    """
    _session = None

    def __init__(self):
        self.executor = ThreadPoolExecutor(1)

    def set_session(self):
        self._session = requests.Session()

    def delete_session(self):
        self._session = None

    def __getattr__(self, name):
        if self._session is not None:
            requests_method = getattr(self._session, name)
        else:
            requests_method = getattr(requests, name)
        return lambda *args, **kwargs: self.executor.submit(requests_method, *args, **kwargs)

    def iter_lines(self, response):
        """Asynchronously iterate through the lines of a response"""
        it = response.iter_lines()
        while True:
            yield self.executor.submit(lambda : next(it))


# async_requests.get = requests.get returning a Future, etc.
async_requests = _AsyncRequests()
