import datetime
import urllib2
import types

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils import simplejson as json

from spotfeedreader.models import SpotFeed, SpotMessage

class Command(BaseCommand):
    help = 'Import the feed data from the feed id defined in the settings under SPOT_FEED_ID'
    
    def handle(self, *args, **kwargs):
		if 'latest' in args:
			url = "https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/%s/latest.json" % settings.SPOT_FEED_ID
		else:
			url = "https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/%s/message.json" % settings.SPOT_FEED_ID
		self.stdout.write('Fetching feed at %s\n' % url)
		data = urllib2.urlopen(url)
		self.stdout.write('Response received\n')
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
					self.save_spot_message(message)
			else:
				self.save_spot_message(obj['response']['feedMessageResponse']['messages']['message'])
		else:
			self.stderr.write('Error\n')
		
    def save_spot_message(self, message):
		self.stdout.write('[%s] %s : lat=%f, lon=%f\n' % (
			message['id'],
			message['unixTime'],
			message['latitude'],
			message['longitude'],
		))
		try:
			spotMessage = SpotMessage.objects.get(spot_message_id=message['id'])
			self.stdout.write('Skip\n')
		except SpotMessage.DoesNotExist:
			if not message.has_key('batteryState'):
				message['batteryState'] = None
			if not message.has_key('altitude'):
				message['altitude'] = 0
			if not message.has_key('hidden'):
				message['hidden'] = 0
			if not message.has_key('modelId'):
				message['modelId'] = None
			
			spotMessage = SpotMessage(
				spot_message_id = message['id'],
				messenger_id = message['messengerId'],
				messenger_name = message['messengerName'],
				unix_time = message['unixTime'],
				date_time = datetime.datetime.utcfromtimestamp(message['unixTime']),
				message_type = message['messageType'],
				latitude = str(message['latitude']),
				longitude = str(message['longitude']),
				model = message['modelId'],
				show_custom_msg = message['showCustomMsg'],
				message_detail = message['messageDetail'],
				altitude = message['altitude'],
				battery = message['batteryState'],
				hidden = message['hidden']
			)
			self.stdout.write('Create\n')
			self.stdout.write('%s\n' % spotMessage)
			spotMessage.save()

