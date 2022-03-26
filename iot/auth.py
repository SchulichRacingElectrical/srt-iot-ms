# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from functools import wraps
from flask import request, abort

def require_api_key(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    key = request.headers.get('apiKey')
    if key == None: abort(401)
    if key == 'a':
      return f(key, *args, **kwargs)
  decorated.__doc__ = f.__doc__
  return decorated