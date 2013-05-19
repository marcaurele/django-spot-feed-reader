import urllib2
import time

from django.conf import settings
from django.core import serializers
from django.http import HttpResponse

from spotfeedreader.models import SpotMessage

def get_last_date_for_data():
	try :
		last_date = settings.SPOT_SITE_STOP_DATE.split('-')
		print settings.SPOT_SITE_STOP_DATE
		last_date_int = [0,0,0,0,0,0,0,0,0]
		for i in range(0,3):
			last_date_int[i] = int(last_date[i])
		print last_date_int
		t = time.mktime(last_date_int)
		print t
		return int(t)
	except :
		return 0

def proxy_feed(request):
	url = "https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/%s/latest.json" % settings.SPOT_FEED_ID
	response = urllib2.urlopen(url)

	# set the body
	content_response = response.read()
	proxy_response = HttpResponse('var spot_message = %s;' % content_response)
	
	# set the headers
	proxy_response['content-type'] = 'application/javascript'
	
	return proxy_response

def latest_point(request):
	last_timestamp = get_last_date_for_data()
	if last_timestamp > 0 :
		latest_point = SpotMessage.objects.filter(messenger_id__exact='0-8197053', unix_time__lte=last_timestamp).order_by('-unix_time')[:1]
	else :
		latest_point = SpotMessage.objects.filter(messenger_id__exact='0-8197053').order_by('-unix_time')[:1]
#	latest_point = resultset[0]
	point_data = serializers.serialize('json', latest_point)
	response = HttpResponse('var spot_message_list = %s;' % point_data)
	return response

def spot_message_as_json(request, nb_of_points=0):
	last_timestamp = get_last_date_for_data()
	if last_timestamp > 0 :
		if nb_of_points <= 0:
			points = SpotMessage.objects.filter(messenger_id__exact='0-8197053', unix_time__lte=last_timestamp).order_by('-unix_time')
		else:
			points = SpotMessage.objects.filter(messenger_id__exact='0-8197053', unix_time__lte=last_timestamp).order_by('-unix_time')[:nb_of_points]
	else :
		if nb_of_points <= 0:
			points = SpotMessage.objects.filter(messenger_id__exact='0-8197053').order_by('-unix_time')
		else:
			points = SpotMessage.objects.filter(messenger_id__exact='0-8197053').order_by('-unix_time')[:nb_of_points]
	
	points_data = serializers.serialize('json', points, fields=(
		'message_id','unix_time','longitude','latitude','message_type',
		))
	#data = serializers.serialize('json', object ,fields=('titi','toto',))
	response = HttpResponse('var spot_message_list = %s;' % points_data);
	return response;