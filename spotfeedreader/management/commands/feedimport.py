import datetime
import urllib2
import types

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils import simplejson as json
from django.utils.timezone import utc

from spotfeedreader.models import SpotFeed, SpotMessage

URL_LATEST = "https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/%s/latest.json"
URL_MESSAGE = "https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/%s/message.json"

class Command(BaseCommand):
    help = 'Import the feed data from the feed id defined in the settings under SPOT_FEED_ID'
    
    def handle(self, *args, **kwargs):
    	# Get all active feeds that we will process
		if 'latest' in args:
			url = URL_LATEST
		else:
			url = URL_MESSAGE
		
		feeds = SpotFeed.objects.filter(active__exact=True)
		if feeds:
			for feed in feeds:
				self.fetch_feed(url % feed.feed_id)
		else:
			self.stdout.write('No active feed to fetch yet')
    
    def fetch_feed(self, url):
		self.stdout.write('Fetching feed at %s\n' % url)
		data = urllib2.urlopen(url)
		obj = json.loads( data.read() )
		if 'feedMessageResponse' in obj['response']:
			# Save the feed information first, only once
			feed = obj['response']['feedMessageResponse']['feed']
			spotFeed, created = SpotFeed.objects.get_or_create(feed_id=feed['id'])
			spotFeed.name = feed['name']
			spotFeed.description = feed['description']
			spotFeed.status = feed['status']
			spotFeed.save()
			if isinstance(obj['response']['feedMessageResponse']['messages']['message'], types.ListType):
				# Iterate on all message to save the new ones if from "message"
				for message in obj['response']['feedMessageResponse']['messages']['message']:
					self.save_spot_message(spotFeed, message)
			else:
				self.save_spot_message(spotFeed, obj['response']['feedMessageResponse']['messages']['message'])
		else:
			self.stderr.write('Error, no data\n')
		
    def save_spot_message(self, spotFeed, message):
		self.stdout.write('[%s] %s : LAT=%f, LON=%f, %s\n' % (
			message['id'],
			message['unixTime'],
			message['latitude'],
			message['longitude'],
			datetime.datetime.utcfromtimestamp(message['unixTime']).replace(tzinfo=utc)
		))
		try:
			spotMessage = SpotMessage.objects.get(message_id=message['id'])
			self.stdout.write('Skip existing with id=%s\n' % message['id'])
		except SpotMessage.DoesNotExist:
			if not message.has_key('messageDetail'):
				message['messageDetail'] = None
			if not message.has_key('showCustomMsg'):
				message['showCustomMsg'] = True
			if not message.has_key('batteryState'):
				message['batteryState'] = None
			if not message.has_key('modelId'):
				message['modelId'] = None
			
			spotMessage = SpotMessage(
				feed = spotFeed,
				message_id = message['id'],
				messenger_id = message['messengerId'],
				messenger_name = message['messengerName'],
				unix_time = message['unixTime'],
				date_time = datetime.datetime.utcfromtimestamp(message['unixTime']).replace(tzinfo=utc),
				message_type = message['messageType'],
				latitude = str(message['latitude']),
				longitude = str(message['longitude']),
				model = message['modelId'],
				show_custom_msg = message['showCustomMsg'],
				message_detail = message['messageDetail'],
				battery = message['batteryState'],
			)
			spotMessage.save()
			self.stdout.write('Created %s\n' % spotMessage)

