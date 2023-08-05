from django.conf import settings
from django.http.response import HttpResponse

DEFAULT_USER_AGENT = ("ELB-HealthChecker/2.0",)


class AWSHealthCheckerResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get('User-Agent', None) in getattr(settings, 'AWS_HEALTH_CHECKER_USER_AGENT', DEFAULT_USER_AGENT):
            return HttpResponse("OK")
        return self.get_response(request)
