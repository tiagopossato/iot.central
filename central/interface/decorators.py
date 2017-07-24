from functools import wraps
from django.http import HttpResponse
import simplejson

def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        json = simplejson.dumps({ 'not_authenticated': True })
        return HttpResponse(json, mimetype='application/json')
    return wrapper