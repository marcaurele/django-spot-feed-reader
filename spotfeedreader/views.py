import urllib2
import time

from django.conf import settings
from django.core import serializers
from django.http import HttpResponse

from spotfeedreader.models import SpotMessage
