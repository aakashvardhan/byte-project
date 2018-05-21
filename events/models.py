from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

import datetime

 


class Schedule(models.Model):
	title = models.CharField(max_length=50)
	day = models.DateField('Date of the Event',help_text="Date")
	start_time = models.TimeField('Time of the Event',help_text="Time")
	venue = models.CharField(max_length=50,null=True)
	notes = models.TextField('Textual Notes',help_text='Textual Notes',blank=True,null=True)
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	attending = models.IntegerField(default=0)
	not_attending = models.IntegerField(default=0)


	def __str__(self):
		return self.title




	class Meta:
		verbose_name = 'Scheduling'
		verbose_name_plural = 'Scheduling'

class Attending(models.Model):
	title = models.CharField(max_length=50,null=True)
	username = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

class NotAttending(models.Model):
	title = models.CharField(max_length=50,null=True)
	username = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

class EventAttendance(models.Model):
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	event_key = models.ForeignKey(Schedule, on_delete=models.CASCADE)

	def __str__(self):
		return "%s - %s" % (self.event_key, self.username)

