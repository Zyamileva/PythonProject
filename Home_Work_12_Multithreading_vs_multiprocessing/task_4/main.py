import http.server
import logging
import socketserver
import threading

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handles HTTP GET requests.

    This class extends SimpleHTTPRequestHandler and overrides the do_GET method
    to handle incoming GET requests in a multi-threaded environment. It sends a
    200 OK response with a plain text message.
    """

    def do_GET(self):
        print(f"Обрабатывается в потоке: {threading.current_thread().name}")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, this is a multi-threaded server!")


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """A multi-threaded HTTP server.

    This class combines ThreadingMixIn and HTTPServer to create an HTTP server
    that handles each request in a separate thread.  It allows for concurrent
    handling of multiple client requests.
    """

    pass


if __name__ == "__main__":
    HOST, PORT = "", 8080

    server = ThreadedHTTPServer((HOST, PORT), MyRequestHandler)

    logging.info(f"Serving on port {PORT}...")

    server.serve_forever()
