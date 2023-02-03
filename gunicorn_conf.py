from multiprocessing import cpu_count

bind = "127.0.0.1:80"

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/fastserver/access_log'
errorlog =  '/home/fastserver/error_log'
