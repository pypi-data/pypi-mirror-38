# -*- coding: utf-8 -*-

import random

import attr
from wsgi_intercept.interceptor import RequestsInterceptor


@attr.s
class Request(object):
    method = attr.ib()
    query = attr.ib()
    headers = attr.ib()
    body = attr.ib(default=None)


class MockWebServer(object):
    def __init__(self, host='', port=None):
        self._host = host or 'localhost'
        self._port = port or random.randint(20000, 50000)
        self._interceptor = RequestsInterceptor(self.get_wsgi_app, host=self._host, port=self._port)
        self._url = 'http://{0}:{1}/'.format(self._host, self._port)

        self._pages = {}

    def get_wsgi_app(self):
        return self.wsgi

    def wsgi(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        path, query = environ['PATH_INFO'], None
        if '?' in path:
            path, query = path.split('?', 1)
        page = self._pages.get(path)
        if not page:
            start_response('404 Not Found', [])
            return []
        body = environ['wsgi.input'].read()
        page.record_request(Request(
            method=method,
            query=query,
            headers=environ.items(),
            body=body,
        ))
        headers = []
        content = [page.content]
        if content:
            headers += [('content-type', page.content_type)]
        start_response('{} {}'.format(page.status, page.status_message), headers)
        return content

    @property
    def url(self):
        return self._url

    def __enter__(self):
        self._interceptor.__enter__()
        return self

    def __exit__(self, *exc):
        self._interceptor.__exit__(*exc)

    def page(self, url):
        import urllib
        if url not in self._pages:
            full_url = urllib.basejoin(self.url, url)
            self._pages[url] = Page(full_url)
        return self._pages[url]

    def set(self, url, content, content_type='text/plain'):
        page = self.page(url)
        page.set_content(content, content_type)
        return page


class Page(object):
    def __init__(self, url):
        self.url = url
        self._content = ''
        self._status = 200
        self._status_message = 'OK'
        self._content_type = ''
        self._requests = []

    def set_content(self, content, content_type):
        if isinstance(content, unicode):
            content = content.encode('utf8')
        self._content = str(content)
        self._content_type = content_type

    @property
    def status(self):
        return self._status

    @property
    def status_message(self):
        return self._status_message

    @property
    def content_type(self):
        return self._content_type

    @property
    def content(self):
        return self._content

    def record_request(self, request):
        self._requests.append(request)

    def request(self, index):
        assert len(self._requests) >= index
        return self._requests[index-1]
