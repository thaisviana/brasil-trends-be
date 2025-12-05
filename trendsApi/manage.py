#!/usr/bin/env python
import os
import sys
import html
from html.parser import HTMLParser

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trendsApi.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    HTMLParser.unescape = html.unescape

    try:
        import django.db.backends.postgresql.base as pg_base
        import pytz
        def utc_tzinfo_factory(offset):
            return pytz.utc
        pg_base.utc_tzinfo_factory = utc_tzinfo_factory
    except ImportError:
        pass

    execute_from_command_line(sys.argv)
