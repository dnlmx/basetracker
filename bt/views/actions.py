from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from utils.logentries import ListLogEntries
from utils.helpers import CurrentUsr

def actions(request):
	template = loader.get_template('actions.html')
	log_entries = ListLogEntries(30)

	context = Context({
		'cuser': CurrentUsr(request.user),		
		'entries': log_entries,
	})
	return HttpResponse(template.render(context))