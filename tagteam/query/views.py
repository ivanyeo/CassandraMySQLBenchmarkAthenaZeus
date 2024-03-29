from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from post.models import Post, Tag, PostTag
from django.shortcuts import get_object_or_404
from query.support_functions import strip_query, getposts
from django.views.decorators.csrf import csrf_exempt
import string
import urllib
import time
from configurations import POST_RETURN_LIMIT

# Configuration
zeus_getpost_url = 'http://zeus.ndnxr.com/query/getpost/'

def my_view(request):
    my_object = get_object_or_404(MyModel, pk=1)
# Create your views here.

def index(request):
    if request.method == 'POST':
        p = Post.objects.get(id=1)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse('Invalid request.')

@csrf_exempt
def processquery(request):
    if request.method == 'POST' and request.POST.dict().has_key('query'):
        query = request.POST.get('query', '')

        # Controller::Application query logic here
        if not query.strip():
            return HttpResponse('Query is blank.')
       
        # Strip query to ensure that it is valid and get sets
        addset, removeset, valid_query = strip_query(query)

        if not valid_query:
            return HttpResponse('Invalid query.')

        # Get top POST_RETURN_LIMIT most recent post within addset-removeset
        start = time.time()
        post_results, err_msg = getposts(addset, removeset, POST_RETURN_LIMIT) 
        end   = time.time()

        time_diff = end - start

        # Insert err_msg followed by time
        post_results.insert(0, Post(text=err_msg)) 
        post_results.insert(0, Post(text=time_diff)) 

        # Return JSON response of query logic
        data = serializers.serialize("json", post_results)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse('Invalid request.')

def getpost(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    data = serializers.serialize("json", [p])
    return HttpResponse(data, content_type="application/json")

def getzeuspost(request, post_id):
    f = urllib.urlopen(zeus_getpost_url + post_id)
    reply = '';

    for line in f:
        reply += line

    f.close()

    return HttpResponse(reply, content_type="application/json")

def getmoreobjects(request):
    p = Posts.objects.filter(text__contains='ivan')[:3]
    return HttpResponse("getmoreobjects() not implemente.")


