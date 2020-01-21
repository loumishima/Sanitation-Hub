from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organisation, Dataset

import random, string

# Information that is going to be displayed on the admin page.

@admin.register(Organisation)
class OrgAdmin(admin.ModelAdmin):
    list_display = ('name', 'codeID', 'isHubMember', 'dateEntrance')
    exclude = ['codeID']
@admin.register(Dataset)
class OrgAdmin(admin.ModelAdmin):
    list_display = ('dateUploaded', 'organisation')

admin.site.register(User, UserAdmin)

