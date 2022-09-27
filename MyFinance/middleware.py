from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class RedirectAnonymousMiddleware:
    """Redirects anonymous users if they aren't on allowed pages."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed = (
            reverse_lazy('main'),
            reverse_lazy('accounts:login'),
            reverse_lazy('accounts:registration'),
        )

    def __call__(self, request):
        return (
            HttpResponseRedirect(reverse_lazy('main'))
            if all([not request.user.is_authenticated, request.path not in self.allowed])
            else self.get_response(request)
            )
