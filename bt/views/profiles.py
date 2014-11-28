from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
#@login_required
#def index(request):
#	template = loader.get_template('admin/profiles/index.html')
#	context = Context({
#		'variable': 'desde vista',
#	})
#	return HttpResponse(template.render(context))

def detail(request, profile_id):
	template = loader.get_template('profiles.html')
	try:
		usr = User.objects.get(pk=profile_id)
	except User.DoesNotExist:
		raise Http404
	
	context = RequestContext(request, {
		'profile_id': profile_id,
		'userprof' : usr
	})	
	return HttpResponse(template.render(context))
