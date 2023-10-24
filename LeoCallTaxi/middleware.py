import uuid


# middleware.py

class PreventBackwardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Store a unique token in the session for each page load
        if 'page_token' not in request.session:
            request.session['page_token'] = uuid.uuid4().hex

        return response
