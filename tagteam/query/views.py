from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from post.models import Post, Tag, PostTag
from django.shortcuts import get_object_or_404
from query.support_functions import strip_query
import string

def my_view(request):
    my_object = get_object_or_404(MyModel, pk=1)
# Create your views here.

def index(request):
	if request.method == 'POST':
		p = Post.objects.get(id=1)
		return HttpResponse(data, content_type="application/json")
	else:
		return HttpResponse('Invalid request.')

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
       
        # Get set of post id
        pids = set()

        #find all post id that has tag in addset
        for addtag in addset:
            t = Tag.objects.get(value=addtag)
            pids = pids.union({ ps.pid_id for ps in PostTag.objects.filter(tid=t.id) })
        for removetag in removeset:
            t = Tag.objects.get(value=removetag)
            pids = pids - { ps.pid_id for ps in PostTag.objects.filter(tid=t.id) }
        #return HttpResponse('Query: {0}'.format(query))
        
        # Return JSON response of query logic
        #return HttpResponse(data, content_type="application/json")
        spids = list(pids)
        spids.sort()
        spids = spids[:10]
        spids = [ str(id) for id in spids ]
        return HttpResponse(string.join(spids, sep=','))
        #p = get_object_or_404(Post, pk=1)
        #data = serializers.serialize("json", [p])
        data = serializers.serialize("json", list(pids))
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse('Invalid request.')

def getpost(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    data = serializers.serialize("json", [p])
    return HttpResponse(data, content_type="application/json")

