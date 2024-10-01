import logging
import uuid

logger = logging.getLogger("info_logger")


class RequestResponseLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the incoming request with the request ID
        try:
            body = request.body.decode("utf-8")
        except AttributeError:
            body = "No body"
        logger.info(f"Incoming Request: {request.method} {request.path} {body}")

        logger.info(
            f"Incoming Request: {request.method} {request.path} {body}"
        )

        # Get the response from the next middleware or view
        response = self.get_response(request)

        # Log the outgoing response with the request ID
        logger.info(
            f"Outgoing Response: {response.status_code} {response.body}"
        )

        return response
