from django.utils.deprecation import MiddlewareMixin

class DisableCSRFForAPIMiddleware(MiddlewareMixin):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.path.startswith('/api_logout/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None