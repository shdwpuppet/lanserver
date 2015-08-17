from social.pipeline.partial import partial
from django.shortcuts import render, render_to_response
from .forms import RegisterForm
from django.http import HttpResponse
from django.contrib.auth.models import User

@partial
def user_register(strategy, details, is_new=False, user=None, *args, **kwargs):
	if is_new:
		if not details.get('new_username'):
			username = strategy.request_data().get('username')
			if username:
				details['username'] = username
			else:
				return