import multiprocessing

# Bind to 0.0.0.0:8000
bind = "0.0.0.0:8000"

# Reload status
reload = False

# Reload status
# reload = False

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Maximum number of simultaneous clients
worker_connections = 1000

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50

# Timeout for graceful workers restart
graceful_timeout = 30

# Timeout for worker processes
timeout = 60

# # Limit the allowed size of an HTTP request body
# limit_request_line = 4096
# limit_request_fields = 100
# limit_request_field_size = 8190

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None
umask = 0


# Logging
# accesslog = "/var/log/gunicorn/access.log"
# errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "gunicorn_django"

# # SSL config
# # keyfile = "/path/to/keyfile"
# # certfile = "/path/to/certfile"


# Django ASGI application
wsgi_app = "core.asgi:application"

# Worker class - use Uvicorn's worker class for ASGI support
worker_class = "uvicorn.workers.UvicornWorker"

# Uvicorn-specific settings
uwsgi_socket = None
http_keepalive = 75
http_timeout = 30
websocket_ping_interval = 20
websocket_ping_timeout = 20
lifespan = "on"


# Server hooks
def on_starting(server):
    pass


def on_reload(server):
    pass


def when_ready(server):
    pass


def on_exit(server):
    pass


# Environment variables
raw_env = [
    "DJANGO_SETTINGS_MODULE=core.settings",
]
