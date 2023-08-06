from django.contrib import admin
from enhanced_emails.models import SentEmail


@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    fields = ["sent_at", "to", ("cc", "bcc"), "content"]
    readonly_fields = ["sent_at", "content", "to", "cc", "bcc"]
