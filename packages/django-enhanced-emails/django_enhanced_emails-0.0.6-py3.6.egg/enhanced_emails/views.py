from django.views.generic.detail import DetailView
from enhanced_emails.models import SentEmail


class EmailView(DetailView):
    model = SentEmail
    template_name = "enhanced_emails/email.html"
