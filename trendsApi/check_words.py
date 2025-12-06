import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trendsApi.settings")
django.setup()

from elections.models import Word

print("Last 10 saved words:")
for w in Word.objects.order_by('-id')[:10]:
    print(f"Text: {w.text}, Period: '{w.period}'")
