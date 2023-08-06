import requests
import os
import json
from functools import wraps
from ..util import base_url, throw_this

def authentication(f):
  @wraps(f)
  def wrapper(self, *args, **kwarg):
      if self.headers:
          return f(self, *args, **kwarg)
      else:
          throw_this('API token not set')
  return wrapper

class APIRequests:
    __instance = None

    @staticmethod 
    def instance():
        if APIRequests.__instance == None:
            APIRequests()
        return APIRequests.__instance

    def __init__(self):
        self.headers = None
        if APIRequests.__instance:
            throw_this('Singleton class: use instance() static method')
        else:
            APIRequests.__instance = self

    def set_api_token(self, api_token):
        self.headers = {'Authorization':  'Bearer %s' % (api_token)}

    @authentication
    def tables_upload_file(self, path, name, overwrite_key=None, append_key=None, column_types=None, column_names=None):
        file_handler = open(path,'rb')
        files = {
          'file': (os.path.basename(path), file_handler, 'multipart/form-data')
        }
        data =  {
          'name': name if name else os.path.basename(path),
          'path': os.path.dirname(path)
        }

        if overwrite_key:
            data['overwriteTableKey'] = overwrite_key
        if append_key:
            data['concatenateTableKey'] = append_key
        if column_types:
            data['columnTypes'] = column_types
        if column_names:
            data['columnNames'] = column_names

        r = requests.post(base_url+'tables.upload', files=files, data=data, headers=self.headers)
        file_handler.close()
        if r.status_code == 200:
            return r.content.decode('utf8')
        else :
            throw_this('tables_upload_file() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

    @authentication
    def tables_upload_data(self, data, name, overwrite_key = None, append_key=None, column_types=None, column_names=None):
        files = {
          'file': (name, data, 'multipart/form-data')
        }
        data =  {
          'name': name
        }
        if overwrite_key:
            data['overwriteTableKey'] = overwrite_key
        if append_key:
            data['concatenateTableKey'] = append_key
        if column_types:
            data['columnTypes'] = column_types
        if column_names:
            data['columnTypes'] = column_names

        r = requests.post(base_url+'tables.upload', files=files, data=data, headers=self.headers)
        if r.status_code == 200:
            return r.content.decode('utf8')
        else :
            throw_this('tables_upload_data() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

    @authentication
    def tables_delete(self, key): 
        payload = {'tableKey' : key}
        r = requests.post(base_url+'tables.delete', json=payload, headers=self.headers)
        if r.status_code == 200:
            return
        else :
            throw_this('tables_delete() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

    @authentication
    def tables_getmetadata(self, key):
        payload = {'tableKey' : key}
        r = requests.post(base_url+'tables.getMetadata', json=payload, headers=self.headers)
        if r.status_code == 200:
            ret = json.loads(r.content.decode('utf8'))
            return (ret['numberColumns'], ret['numberRows'])
        else :
            throw_this('tables_getmetadata() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

    @authentication
    def tables_getcolumns(self, key):
        payload = {'tableKey' : key}
        r = requests.post(base_url+'tables.getColumns', json=payload, headers=self.headers)
        if r.status_code == 200:
            columns = json.loads(r.content.decode('utf8'))
            return columns
        return throw_this('tables_getcolumns() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

    @authentication
    def tables_addnotebook(self, key, query):
        payload = {'tableKey' : key, 'query': query}
        r = requests.post(base_url+'tables.addNotebook', json = payload, headers=self.headers)
        if r.status_code == 200:
            ret = r.content.decode('utf8')
            return json.loads(ret)['notebookKey']
        else :
            throw_this('tables_addnotebook() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

    @authentication
    def tables_getnotebook_metadata(self, notebook_key):
        payload = {'notebookKey' : notebook_key}
        r = requests.post(base_url+'notebooks.getMetadata', json=payload, headers=self.headers)
        if r.status_code == 200:
            return json.loads(r.content.decode('utf8'))
        else :
            throw_this('tables_getnotebook_metadata() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )
        return

    @authentication
    def tables_getdata(self, key, query, offset=None, limit=None):
        payload = {'tableKey' : key, 'query': query}
        if offset:
            payload['offset'] = offset
        if limit:
            payload['limit'] = limit
        r = requests.post(base_url+'tables.getData', json=payload, headers=self.headers)
        if r.status_code == 200:
            return r.content
        else :
            throw_this('tables_getdata() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )
        return

    @authentication
    def auth_getstate(self, visual_key, workspace_id):
        payload = {'notebookKey' : visual_key, 'workspaceId': workspace_id}
        r = requests.post(base_url+'auth.getState', json=payload, headers=self.headers)
        if r.status_code == 200:
            return json.loads(r.content.decode('utf8'))
        else :
            throw_this('auth_getstate() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )
        return

    @authentication
    def users_getprofile(self):
        headers = self.headers
        headers['Content-Type'] = 'application/json'
        r = requests.post(base_url+'users.getProfile', headers=headers)
        if r.status_code == 200:
            return json.loads(r.content.decode('utf8'))
        else :
            throw_this('users_getprofile() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )
        return