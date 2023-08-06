# -*- coding: utf-8 -*-
"""
Base model of Key-Text option storage
"""

from __future__ import unicode_literals

from json import loads as json_loads
from json import dumps as json_dumps

from django.db import models


class BaseKeyTextOptions(models.Model):
	option_key = models.CharField(max_length=128, primary_key=True)
	option_value = models.TextField(blank=True)

	@classmethod
	def get_integer(cls, option_key, default_value=None, min_value=None, max_value=None):
		try:
			v = cls.objects.get(option_key=option_key).option_value
			v = int(v)
			if (max_value is not None) and (v > max_value):
				return max_value
			if (min_value is not None) and (v < min_value):
				return min_value
			return v
		except Exception:
			pass
		return default_value

	@classmethod
	def put_integer(cls, option_key, option_value):
		option_value = str(option_value) if isinstance(option_value, int) else ''
		cls.objects.update_or_create(option_key=option_key, defaults={'option_value': option_value})

	@classmethod
	def get_json_object(cls, option_key, default_value=None):
		try:
			v = cls.objects.get(option_key=option_key).option_value
			if v:
				return json_loads(v)
		except Exception:
			pass
		return default_value

	@classmethod
	def put_json_object(cls, option_key, option_object, *args, **kwds):
		option_value = json_dumps(option_object, *args, **kwds)
		cls.objects.update_or_create(option_key=option_key, defaults={'option_value': option_value})

	@classmethod
	def get_text(cls, option_key, default_value=None):
		try:
			return cls.objects.get(option_key=option_key).option_value
		except Exception:
			pass
		return default_value

	@classmethod
	def put_text(cls, option_key, option_value):
		option_value = option_value if isinstance(option_value, basestring) else str(option_value)
		cls.objects.update_or_create(option_key=option_key, defaults={'option_value': option_value})

	def __unicode__(self):
		return "%s(option_key=%r, option_value=%r)" % (
				self.__class__.__name__,
				self.option_key,
				self.option_value,
		)

	class Meta:
		abstract = True
