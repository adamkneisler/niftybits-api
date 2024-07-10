from django.contrib import admin
from .models import *


admin.site.register(NiftyUser)
admin.site.register(Deposit)
admin.site.register(Withdrawl)
admin.site.register(Ledger)