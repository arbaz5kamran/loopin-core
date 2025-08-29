# Gunicorn configuration optimized for Railway memory constraints
import multiprocessing
import os

# Railway-optimized worker configuration (memory-efficient)
# Railway typically provides 512MB-1GB, so we need to be conservative
cpu_count = multiprocessing.cpu_count()
if cpu_count > 1:
    workers = 2  # Fixed at 2 workers for Railway
else:
    workers = 1

# Environment-specific configuration
is_production = os.getenv("RAILWAY_ENVIRONMENT") == "production" or os.getenv("FLASK_ENV") == "production"
if is_production:
    # Production optimizations
    loglevel = 'warning'  # Less verbose in production
    accesslog = None  # Disable access log in production
    errorlog = None  # Disable error log in production (use Railway logs)
else:
    # Development settings
    loglevel = 'info'
    accesslog = '-'
    errorlog = '-'

worker_class = 'gevent'  # Use gevent for better memory efficiency
threads = 1  # Reduce threads
timeout = 30  # Shorter timeout to free memory faster
keepalive = 10  # Shorter keepalive

# Memory optimization
preload_app = True  # Preload app to share memory
max_requests = 500  # Restart worker after fewer requests
max_requests_jitter = 50
worker_connections = 100  # Reduce connections per worker

# Railway-specific optimizations
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
backlog = 128  # Smaller backlog
graceful_timeout = 15  # Faster graceful shutdown

# Logging (keep minimal for memory)
accesslog = '-'
errorlog = '-'
loglevel = 'warning'  # Less verbose logging

# Security (keep minimal)
limit_request_line = 4094
limit_request_fields = 50  # Reduced
limit_request_field_size = 4096  # Reduced

# Process naming
proc_name = 'loopin'

def on_starting(server):
    """Log when the server starts."""
    server.log.info("Starting Loopin server")

def when_ready(server):
    """Log when the server is ready."""
    server.log.info("Loopin server is ready")

def worker_abort(worker):
    """Log when a worker is aborted."""
    worker.log.warning("Worker aborted - possible memory issue")

def on_reload(server):
    """Log when server is reloaded."""
    server.log.info("Server reloaded")

def post_fork(server, worker):
    """Log after worker fork."""
    server.log.info(f"Worker {worker.pid} forked")

def pre_fork(server, worker):
    """Log before worker fork."""
    server.log.info(f"Forking worker {worker.pid}")

def worker_int(worker):
    """Log when worker receives INT signal."""
    worker.log.info("Worker received INT signal")
