# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from functools import wraps
from flask import request, abort

def __key_valid(key):
  # TODO: Request the gateway to check if the key is valid
  # Only need to do this for requests coming directly from the hardware
  return True

def require_api_key(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    key = request.headers.get('apiKey')
    if key == None: abort(401)
    if __key_valid(key):
      return f(key, *args, **kwargs)
  decorated.__doc__ = f.__doc__
  return decorated