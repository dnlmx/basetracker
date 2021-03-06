from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from utils.logentries import ListLogEntries


def actions(request):
	template = loader.get_template('actions.html')
	log_entries = ListLogEntries(30)

	context = RequestContext(request, {
		'entries': log_entries,
	})
	return HttpResponse(template.render(context))