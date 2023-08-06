"""Custom middleware for the auditlogger app"""
import threading
import uuid


class AuditLoggerMiddleware(object):
    """Custom middleware to fetch request data"""
    # Save current request
    _request = {}  # type: ignore

    def process_request(self, request):  # type () -> None
        """
        Add unique id to request, this way we can group them later.
        """
        request.id = uuid.uuid4().hex
        self.__class__.set_request(request)

    def process_response(self, _, response):  # type () -> None
        """Delete request"""
        self.__class__.del_request()
        return response

    def process_exception(self, _, __):  # type () -> None
        """Delete request"""
        self.__class__.del_request()

    @classmethod
    def get_request(cls, default=None):
        """Retrieve request"""
        return cls._request.get(threading.current_thread(), default)

    @classmethod
    def set_request(cls, request):
        """Store request"""
        cls._request[threading.current_thread()] = request

    @classmethod
    def del_request(cls):
        """Delete request"""
        cls._request.pop(threading.current_thread(), None)
