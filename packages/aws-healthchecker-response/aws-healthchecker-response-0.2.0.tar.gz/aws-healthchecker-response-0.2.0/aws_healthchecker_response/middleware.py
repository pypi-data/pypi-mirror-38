from django.conf import settings
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin

DEFAULT_USER_AGENT = ("ELB-HealthChecker/2.0",)


class AWSHealthCheckerResponseMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.META.get('User-Agent', None) in getattr(settings, 'AWS_HEALTH_CHECKER_USER_AGENT', DEFAULT_USER_AGENT):
            return HttpResponse("OK")
        return self.get_response(request)
