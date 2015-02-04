from django.contrib import admin

# Register your models here.
from .models import  Membership, Transaction, UserMerchantId

admin.site.register(Membership)
admin.site.register(Transaction)
admin.site.register(UserMerchantId)