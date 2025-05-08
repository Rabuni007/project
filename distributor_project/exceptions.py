from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data format
        customized_response = {
            'error': {
                'type': exc.__class__.__name__,
                'detail': response.data,
                'status_code': response.status_code,
            }
        }
        response.data = customized_response
    else:
        # Handle unexpected exceptions
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        response = Response(
            {
                'error': {
                    'type': exc.__class__.__name__,
                    'detail': 'An unexpected error occurred.',
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
