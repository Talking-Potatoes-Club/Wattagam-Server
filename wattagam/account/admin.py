from django.contrib import admin

# Register your models here.
import account

admin.site.register(account.models.Account)
