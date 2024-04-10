from django.contrib import admin
from .models import SupportTicket, SupportTicketAdmin

class SupportTicketAdmin(admin.ModelAdmin):
    # Define admin configuration for SupportTicket model
    pass

admin.site.register(SupportTicket,SupportTicketAdmin)
