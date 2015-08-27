# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render_to_response
from xfeed.models import Feed

__author__ = 'Ruud Schroën'
__copyright__ = 'Copyright 2015, Ruud Schroën'
__license__ = 'BSD'
__version__ = '0.5'
__maintainer__ = 'Ruud Schroën'
__email__ = 'schroenruud@gmail.com'
__status__ = 'Development'

def detail(request, uuid):
    try:
        f = Feed.objects.get(uuid=uuid)
    except Feed.DoesNotExist:
        raise Http404("Feed does not exist")
    return render_to_response('xfeed/detail.html', {'feed': f})
