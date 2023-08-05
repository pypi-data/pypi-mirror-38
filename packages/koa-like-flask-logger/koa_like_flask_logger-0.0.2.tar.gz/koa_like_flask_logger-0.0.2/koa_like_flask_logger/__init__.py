from flask import g, request
from time import time

gray = '\x1b[90m'
bold = '\x1b[1m'
normal = '\x1b[m'
red = '\x1b[31m'
green = '\x1b[32m'
yellow = '\x1b[33m'
blue = '\x1b[34m'
cyan = '\x1b[36m'

def register(app):
    @app.before_request
    def log_api_start():
        g._api_start = time()
        status = '%s<~~%s' % (gray, normal)
        method = '%s%s%s' % (bold, request.method, normal)
        path = '%s%s%s' % (gray, request.path, normal)
        print(' '.join([' ', status, method, path]))

    @app.after_request
    def log_api_end(response):
        api_time = time() - g._api_start
        status_color = [red, blue, green, cyan, yellow, red]
        status = (
            ('%s~~>%s' % (gray, normal))
            if response.status_code != 500
            else ('%sxxx%s' % (red, normal))
        )
        method = '%s%s%s' % (bold, request.method, normal)
        path = '%s%s%s' % (gray, request.path, normal)
        status_code = '%s%d%s' % (
            status_color[response.status_code // 100],
            response.status_code,
            normal,
        )
        duration = '%s%s%s' % (
            gray,
            (
                '%dms' % (api_time * 1000)
                if api_time < 10
                else '%.3g' % api_time
            ),
            normal,
        )
        if response.is_sequence:
            raw_size = sum(map(len, response.iter_encoded()))
            if raw_size > 1024 * 1024:
                size = '%.3gmb' % (raw_size / (1024 * 1024))
            elif raw_size > 1024:
                size = '%.3gkb' % (raw_size / 1024)
            else:
                size = '%db' % raw_size
        else:
            size = 'streamed' if response.is_streamed else 'likely-streamed'
        length = '%s%s%s' % (gray, size, normal)

        print(
            ' '.join(
                [' ', status, method, path, status_code, duration, length]
            )
        )

        return response
