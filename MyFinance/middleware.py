from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class RedirectAnonymousMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    allowed = [
            reverse_lazy('main'),
            reverse_lazy('accounts:login'),
            reverse_lazy('accounts:registration'),
        ]

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in self.allowed:
            return HttpResponseRedirect(reverse_lazy('main'))
        response = self.get_response(request)
        return response
