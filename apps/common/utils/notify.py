from django.contrib import messages

class Notify:
    def notify(self, request, message, level = 'success'):
        levels = {
            'success' : messages.SUCCESS,
            'warning' : messages.WARNING,
            'error' : messages.ERROR,
            'critical' : messages.ERROR,
            'info' : messages.INFO,
            'debug' : messages.DEBUG,
        }
        messages.add_message(request=request, level=levels[level], message=message)