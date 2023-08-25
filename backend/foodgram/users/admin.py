from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User, Subscribe

admin.site.register(User)
admin.site.register(Subscribe)
admin.site.unregister(Group)
