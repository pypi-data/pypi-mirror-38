from .headers cimport HttpHeader, HttpHeaderCollection
from .messages cimport HttpRequest, HttpResponse
from .scribe cimport is_small_response, write_small_response
from .scribe import write_response


include "includes/consts.pxi"


import time
import httptools
from asyncio import Event
from httptools.parser.errors import HttpParserCallbackError, HttpParserError


cdef class ConnectionHandler:
    
    def __init__(self, *, object app, object loop):
        self.app = app
        self.max_body_size = app.options.limits.max_body_size
        app.connections.add(self)
        self.time_of_last_activity = time.time()
        self.loop = loop
        self.transport = None
        self.reading_paused = False
        self.writing_paused = False
        self.writable = Event()
        self.closed = False

        self.parser = httptools.HttpRequestParser(self)
        self.url = None
        self.method = None
        self.request = None  # type: HttpRequest
        self.headers = []

    def reset(self):
        self.request = None
        self.parser = httptools.HttpRequestParser(self)
        self.reading_paused = False
        self.writing_paused = False
        self.url = None
        self.method = None
        self.headers = []

    def pause_reading(self):
        self.reading_paused = True
        self.transport.pause_reading()

    def resume_reading(self):
        self.reading_paused = False
        self.transport.resume_reading()

    def pause_writing(self):
        self.writing_paused = True

    def resume_writing(self):
        if self.writing_paused:
            self.time_of_last_activity = time.time()
            self.writing_paused = False
            self.writable.set()

    def connection_made(self, transport):
        self.time_of_last_activity = time.time()
        self.transport = transport

    def connection_lost(self, exc):
        if self.request:
            self.request.active = False
        self.app.connections.discard(self)
        self.close()
        self.reset()

    def close(self):
        if not self.closed:
            self.closed = True
            if self.transport:
                self.transport.write(b'\r\n\r\n')
                self.transport.close()

    def data_received(self, bytes data):
        self.time_of_last_activity = time.time()

        try:
            self.parser.feed_data(data)
        except HttpParserCallbackError:
            self.close()
        except HttpParserError:
            # ignore: this can happen for example if a client posts a big request to a wrong URL;
            # we return 404 immediately; but the client sends more chunks; http-parser.c throws exception
            # in this case
            pass

    def get_client_ip(self):
        return self.transport.get_extra_info('peername')[0]

    def handle_invalid_request(self, message):
        self.transport.write(message)
        self.close()

    def on_body(self, bytes value):
        self.request.on_body(value)

        body_len = len(self.request.raw_body)

        if body_len > self.max_body_size:
            self.handle_invalid_request(b'Exceeds maximum body size')

    def on_headers_complete(self):
        cdef HttpRequest request
        request = HttpRequest(
            self.method,
            self.url,
            HttpHeaderCollection(self.headers),
            None
        )
        # TODO: think of a lazy way to get client_ip: client ip is not always interesting
        # request.client_ip = self.get_client_ip()
        self.request = request
        self.loop.create_task(self.handle_request(request))

    def on_url(self, bytes url):
        self.url = url
        self.method = self.parser.get_method()

    def on_header(self, bytes name, bytes value):
        self.headers.append(HttpHeader(name, value))

        if len(self.headers) > MAX_REQUEST_HEADERS_COUNT or len(value) > MAX_REQUEST_HEADER_SIZE:
            self.transport.write(write_small_response(HttpResponse(413)))
            self.reset()
            self.close()

    async def handle_request(self, HttpRequest request):
        response = await self.app.handle(request)
        if not isinstance(response, HttpResponse):
            raise RuntimeError(f'The application handler for path {request.url.path} did not return an HttpResponse!')
        await self._send_response(response)

    async def get_response(self):
        return await self.app.handle(self.request)

    async def _send_response(self, HttpResponse response):
        cdef bytes chunk

        if is_small_response(response):
            chunk = write_small_response(response)
            self.transport.write(chunk)
        else:
            async for chunk in write_response(response):
                if self.writing_paused:
                    await self.writable.wait()
                self.transport.write(chunk)

        if not self.parser.should_keep_alive():
            self.close()
        self.reset()
