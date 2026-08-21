import os
from django.core.wsgi import get_wsgi_application
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_app = get_wsgi_application()

class DebugEnvMiddleware:
    """WSGI middleware to serve debug endpoint before Django validation"""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Intercept /debug/env/ requests
        if environ['PATH_INFO'] == '/debug/env/':
            try:
                log_path = os.path.join(Path(__file__).resolve().parent.parent, 'django_startup_debug.log')
                if os.path.exists(log_path):
                    with open(log_path, 'r') as f:
                        content = f.read()
                    start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
                    return [content.encode('utf-8')]
                else:
                    start_response('404 Not Found', [('Content-Type', 'text/plain')])
                    return [b'Debug log not found']
            except Exception as e:
                start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
                return [f'Error: {str(e)}'.encode('utf-8')]

        # Pass all other requests to Django
        return self.app(environ, start_response)

application = DebugEnvMiddleware(django_app)
