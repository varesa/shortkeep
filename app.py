import os
import re

from flask import Flask, abort, request
import redis


if 'REDIS_URL' in os.environ.keys():
    REDIS_URL = os.environ['REDIS_URL']
else:
    REDIS_URL = "localhost"

print(f"Using {REDIS_URL} as redis URL")


app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)


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

app.run()