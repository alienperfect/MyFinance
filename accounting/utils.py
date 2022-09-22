def is_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True
