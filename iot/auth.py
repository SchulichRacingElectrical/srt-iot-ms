# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from functools import wraps
from flask import request, abort

def require_api_key(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    key = request.headers.get('Authorization')
    if key == None: abort(401)
    # Validate the api key with the gateway
    # Make request to the api gateway either with the API key or jwt
    
    return f(key, *args, **kwargs)
  return decorated