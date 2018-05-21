from django.contrib import admin

from .models import Schedule, EventAttendance
from .models import Attending
from .models import NotAttending

# Register your models here.


admin.site.register(Schedule)
admin.site.register(Attending)
admin.site.register(NotAttending)
admin.site.register(EventAttendance)