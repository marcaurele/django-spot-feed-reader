from django.db import models

class SpotFeed(models.Model):
	'''
	Represents the object return in the JSON/XML object from spot API
	'''
	ACTIVE_CHOICES = (
		(True, 'yes'),
		(False, 'no'),
	)
	# Feed ID
	feed_id = models.CharField('feed id', max_length=128, db_index=True, unique=True)
	# Status on/off if the feed should be retrieved
	active = models.BooleanField('fetch data feed?', default=True, db_index=True, choices=ACTIVE_CHOICES)
	# Date when imported
	created_date = models.DateTimeField('created date', auto_now_add=True)
	
	# un-editable fields, fetch from the feed automatically
	# Feed name
	name = models.CharField('feed name', max_length=128, blank=True)
	# Feed description
	description = models.CharField('feed description', max_length=512, blank=True)
	# Status of the feed (ACTIVE, ...) from spot
	status = models.CharField('status', max_length=32, blank=True, editable=False)
	
	class Meta:
		verbose_name = 'spot feed'
	
	def __unicode__(self):
		return '[%d] %s - %s' % (
			self.id,
			self.name,
			self.feed_id,
		)

class SpotMessage(models.Model):
	'''
	Represents the message object returned by the Spot API service
	'''
	# Spot feed ID
	feed = models.ForeignKey(SpotFeed, verbose_name='related feed', related_name='messages')
	# Spot message ID
	message_id = models.PositiveIntegerField('message id')
	# Messenger ID
	messenger_id = models.CharField('messenger id', max_length=32)
	# Messenger Name field
	messenger_name = models.CharField('messenger name', max_length=256, blank=True)
	# Unix time of spot message
	unix_time = models.IntegerField('unix timestamp', db_index=True)
	# Date time value of the unix timestamp
	date_time = models.DateTimeField('date time UTC', db_index=True)
	# Message type
	message_type = models.CharField('message type', max_length=32)
	# Latitude position
	latitude = models.DecimalField('latitude', max_digits=8, decimal_places=5)
	# Longitude position
	longitude = models.DecimalField('longitude', max_digits=8, decimal_places=5)
	# Spot device model name
	model = models.CharField('spot device model', max_length=32, blank=True, null=True)
	# showCustomMessage field
	show_custom_msg = models.BooleanField('show custom message', default=True)
	# Message detail
	message_detail = models.TextField('message detail', blank=True, null=True)
	# Altitude
	# NOT IN THE FEED ANYMORE as of 06.05.2013
	#altitude = models.IntegerField('altitude', default=0)
	# Hidden field - always is 0, why should I bother saving it?
	#hidden = models.BooleanField('hidden')
	# Battery status
	battery = models.CharField('battery status', max_length=32, blank=True, null=True)
	# Date when imported
	created_date = models.DateTimeField('created date', auto_now_add=True)
	
	class Meta:
		verbose_name = 'spot message'
	
	def __unicode__(self):
		return '[%d] %d - %d' % (self.id, self.feed.id, self.message_id)

