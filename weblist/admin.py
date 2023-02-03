from django.contrib import admin

from .models import WebLink
from .models import YoutubeLink

admin.site.register(WebLink)
admin.site.register(YoutubeLink)