from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.shortcuts import render_to_response
from xfeed.models import Feed

def detail(request, uuid):
    try:
        f = Feed.objects.get(uuid=uuid)
    except Feed.DoesNotExist:
        raise Http404("Feed does not exist")
    return render_to_response('xfeed/detail.html', {'feed': f})