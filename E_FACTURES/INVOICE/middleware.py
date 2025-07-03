# ton_app/middleware.py
class AllowIframeForMediaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/media/'):
            # 1. Supprimer X-Frame-Options
            response.headers.pop('X-Frame-Options', None)
            # 2. Supprimer d'autres headers si existants
            response.headers.pop('Content-Security-Policy', None)

        return response
