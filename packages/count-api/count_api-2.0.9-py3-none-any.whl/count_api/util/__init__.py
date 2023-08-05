from functools import wraps
import os

base = 'https://count.co'

try:
    base = os.environ['COUNT_URL']
except:
    pass

base_url = '%s/api/v1/' % (base)
base_return_url = '%s/explore' % (base)
base_embed_url = '%s/embed' % (base)
base_preview_url = '%s/api/v1/notebooks.getPreview' % (base)

def throw_this(msg):
  raise Exception('CountAPI: ' + msg)

def print_this(msg):
  print('CountAPI: ' + msg)

def authentication(f):
  @wraps(f)
  def wrapper(self, *args, **kwarg):
      if self.headers:
          return f(self, *args, **kwarg)
      else:
          throw_this('Error: API token not set')
  return wrapper