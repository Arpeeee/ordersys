import logging

logger = logging.getLogger('django.request')


class RequestHeaderLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            logger.debug(
                'POST %s | Host=%s | Origin=%s | Referer=%s | X-Forwarded-Proto=%s',
                request.path,
                request.META.get('HTTP_HOST', '-'),
                request.META.get('HTTP_ORIGIN', '-'),
                request.META.get('HTTP_REFERER', '-'),
                request.META.get('HTTP_X_FORWARDED_PROTO', '-'),
            )
        return self.get_response(request)
