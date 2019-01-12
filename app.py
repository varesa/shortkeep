import os
import re

from flask import Flask, abort, request
import redis


if 'REDIS_HOSTL' in os.environ.keys():
    REDIS_HOST = os.environ['REDIS_HOST']
else:
    REDIS_HOST = "localhost"

print(f"Using {REDIS_HOST} as redis URL")


app = Flask(__name__)
r = redis.Redis(host=REDIS_HOST, port=6379, db=0)


def apply_suffix(number, suffix):
    number = int(number)
    if suffix == 'm':
        return number * 60
    if suffix == 'h':
        return number * 60 * 60
    if suffix == 'd':
        return number * 60 * 60 * 24
    return number


@app.route('/<key>/<timeout>', methods=['POST'])
def post(key, timeout):
    number, suffix = re.match("([0-9]+)([mhd]?)", timeout).groups()
    timeout_seconds = apply_suffix(number, suffix)

    r.set(key, request.get_data())
    print(key, timeout_seconds)
    r.expire(key, timeout_seconds)

    return "OK"


@app.route('/<key>', methods=['GET'])
def get(key):
    content = r.get(key)

    if content is None:
        return abort(404)
    else:
        return content


@app.route('/health')
def health():
    r.set('health', 111)
    r.incr('health')
    if r.get('health') == b'112':
        return 'OK'
    else:
        return abort(500)

app.run(host="0.0.0.0")
