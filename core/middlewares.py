import logging
import uuid

logger = logging.getLogger("info_logger")


class RequestResponseLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate a unique request ID
        request_id = str(uuid.uuid4())

        # Attach the request ID to the request object for future access
        request.request_id = request_id

        # Log the incoming request with the request ID
        logger.info(
            f"[Request ID: {request_id}] Incoming Request: {request.method} {request.path}"
        )

        # Get the response from the next middleware or view
        response = self.get_response(request)

        # Log the outgoing response with the request ID
        logger.info(
            f"[Request ID: {request_id}] Outgoing Response: {response.status_code}"
        )

        return response
