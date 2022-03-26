# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from functools import wraps
from flask import request, abort

def require_api_key(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    key = request.headers.get('Authorization')
    if key == None: abort(401)
    if key == 'a':
      return f(key, *args, **kwargs)
  return decorated