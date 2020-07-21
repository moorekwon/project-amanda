daemon = False
chdir = '/srv/amanda/app'
bind = 'unix:/run/amanda.sock'
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'

# Redirect stdout/stderr to specified file in errorlog
capture_output = True
