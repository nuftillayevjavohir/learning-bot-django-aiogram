from django.urls import path

from apps.bot.views import WebhookView

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook')
]
