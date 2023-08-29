from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    list_display_links = ('id', 'email', 'username')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe)
admin.site.unregister(Group)
