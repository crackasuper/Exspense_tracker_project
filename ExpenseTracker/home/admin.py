from django.contrib import admin
from .models import AddMoney, UserProfile
from django.contrib.sessions.models import Session
from django.contrib import admin
class AddMoneyAdmin(admin.ModelAdmin):
    list_display = ['user', 'quantity', 'Date', 'catagory', 'add_money']
admin.site.register(AddMoney, AddMoneyAdmin)
admin.site.register(UserProfile)
admin.site.register(Session)
