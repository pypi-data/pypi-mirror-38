from django.conf import settings
from django.views import debug


def get_search_url():
    default_choice = "google"

    search_urls = {
        "google": "https://www.google.com/search?q="
                  "+django+{{ exception_value|force_escape }}",
        "stackoverflow": "http://stackoverflow.com/search?q="
                         "{{ exception_value|force_escape }}",
    }

    search_url = getattr(
        settings,
        'DJANGO_TRACE_SEARCH_SITE',
        default_choice
    )

    return search_urls.get(search_url, search_urls[default_choice])


def _patch_django_debug_view():
    new_data = """
        <button style="margin-bottom:10px; background: #c33a1b; border: 2px solid #560909; padding: 4px 8px; border-radius: 3px;">
            <a href="{}"
                 target="_blank" 
                 style="color: #f5f5f5; text-decoration: none; font-size: 1rem; font-weight: bold;">
                 Search the solve
             </a>
        </button>
    """.format(get_search_url())

    insert_before = '<table class="meta">'
    replacement = new_data + insert_before

    if hasattr(debug, 'TECHNICAL_500_TEMPLATE'):
        if new_data in debug.TECHNICAL_500_TEMPLATE:
            return
        debug.TECHNICAL_500_TEMPLATE = debug.TECHNICAL_500_TEMPLATE.replace(insert_before, replacement, 1)
    else:
        from pathlib import Path
        from django.template import Context

        def new_get_traceback_html(exception_reporter):
            """Return HTML version of debug 500 HTTP error page."""
            with Path(debug.CURRENT_DIR, 'templates', 'technical_500.html').open() as fh:
                template_string = fh.read()
                template_string = template_string.replace(insert_before, replacement, 1)
                t = debug.DEBUG_ENGINE.from_string(template_string)
            c = Context(exception_reporter.get_traceback_data(), use_l10n=False)
            return t.render(c)

        debug.ExceptionReporter.get_traceback_html = new_get_traceback_html


class ErrorSearchMiddleware:

    def __init__(self, get_response):
        # A middleware factory is a callable that takes a get_response callable and returns a middleware.
        # A middleware is a  callable that takes a request and returns a response, just like a view.

        self.get_response = get_response
        _patch_django_debug_view()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
