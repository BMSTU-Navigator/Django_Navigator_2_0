from django.contrib import admin
from Navigator.models import *
# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(Point)
admin.site.register(Instance)
admin.site.register(GraphConnection)
admin.site.register(Dialogs)