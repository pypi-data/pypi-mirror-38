# -*- coding: utf-8 -*-
"""
Utilities for setting up Django model field
"""

from __future__ import unicode_literals


def _make_default_kwd_method(orig_method, k, v):
	""" (internal)
	"""

	def f(self, *args, **kwds):
		kwds.setdefault(k, v)
		return orig_method(self, *args, **kwds)

	return f


def _make_default_kwd_modelfield_deconstruct(orig_deconstruct, k, v):
	""" (internal)
	"""

	def f(self, *args, **kwds):
		name, path, dargs, dkwds, = orig_deconstruct(self, *args, **kwds)
		if not (dkwds.get(k) is v):
			del dkwds[k]
		return name, path, dargs, dkwds

	return f


def attach_default_help_text(help_text):
	"""
	Decorator to attach default help text for model field

	Args:
		help_text - Help text
	"""

	def f(cls):
		cls.__init__ = _make_default_kwd_method(cls.__init__, "help_text", help_text)
		cls.deconstruct = _make_default_kwd_modelfield_deconstruct(cls.deconstruct, "help_text", help_text)
		return cls

	return f
