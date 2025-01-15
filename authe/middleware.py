from django.utils.deprecation import MiddlewareMixin
from .models import UserRegistration

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                request.user = UserRegistration.objects.get(pk=user_id)
            except UserRegistration.DoesNotExist:
                request.user = None
        else:
            request.user = None