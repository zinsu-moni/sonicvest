"""
WSGI entry point for production deployment
Handles static file serving for Vercel and other platforms
"""
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.shared_data import SharedDataMiddleware
from app import app

# Ensure static files are served properly
static_folder = os.path.join(os.path.dirname(__file__), 'static')
if os.path.exists(static_folder):
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/static': static_folder
    })

# Fix for reverse proxies (Vercel, Heroku, etc.)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

if __name__ == '__main__':
    app.run()
