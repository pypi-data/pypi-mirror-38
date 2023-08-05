import requests
import os
import json

from ..util import base_url

def throw_this(msg):
  raise Exception('CountAPI: ' + msg)

def tables_upload_file(headers, path, name, overwrite_key=None, append_key=None, column_types=None, column_names=None):
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

    r = requests.post(base_url+'tables.upload', files=files, data=data, headers=headers)
    file_handler.close()
    if r.status_code == 200:
        return r.content.decode('utf8')
    else :
        throw_this('Error: overwrite received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

def tables_upload_data(headers, data, name, overwrite_key = None, append_key=None, column_types=None, column_names=None):
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

    r = requests.post(base_url+'tables.upload', files=files, data=data, headers=headers)
    if r.status_code == 200:
        return r.content.decode('utf8')
    else :
        throw_this('Error: overwrite received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

def tables_delete(headers, key): 
    payload = {'tableKey' : key}
    r = requests.post(base_url+'tables.delete', json=payload, headers=headers)
    if r.status_code == 200:
        return
    else :
        throw_this('Error: delete() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

def tables_getmetadata(headers, key):
    payload = {'tableKey' : key}
    r = requests.post(base_url+'tables.getMetadata', json=payload, headers=headers)
    if r.status_code == 200:
        ret = json.loads(r.content.decode('utf8'))
        return (ret['numberColumns'], ret['numberRows'])
    else :
        throw_this('Error: size() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

def tables_getcolumns(headers, key):
    payload = {'tableKey' : key}
    r = requests.post(base_url+'tables.getColumns', json=payload, headers=headers)
    if r.status_code == 200:
        columns = json.loads(r.content.decode('utf8'))
        return columns
    return throw_this('Error: received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

def tables_addnotebook(headers, key, query):
    payload = {'tableKey' : key, 'query': query}
    r = requests.post(base_url+'tables.addNotebook', json = payload, headers=headers)
    if r.status_code == 200:
        ret = r.content.decode('utf8')
        return json.loads(ret)['notebookKey']
    else :
        throw_this('Error: upload_visual received response %s: %s' % (r.status_code,r.content.decode('utf8')) )

def tables_getnotebook_metadata(headers, notebook_key):
    payload = {'notebookKey' : notebook_key}
    r = requests.post(base_url+'notebooks.getMetadata', json=payload, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content.decode('utf8'))
    else :
        throw_this('Error: get_notebook_metadata received response %s: %s' % (r.status_code,r.content.decode('utf8')) )
    return

def tables_getdata(headers, key, query, offset, limit):
    payload = {'tableKey' : key, 'query': query, offset: offset, limit: limit}
    r = requests.post(base_url+'tables.getData', json=payload, headers=headers)
    if r.status_code == 200:
        return r.content
    else :
        throw_this('Error: head() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )
    return

def auth_getstate(headers, visual_key, workspace_id):
    payload = {'notebookKey' : visual_key, 'workspaceId': workspace_id}
    r = requests.post(base_url+'auth.getState', json=payload, headers=headers)
    if r.status_code == 200:
        return json.loads(r.content.decode('utf8'))
    else :
        throw_this('Error: head() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )
    return

def users_getprofile(headers):
    headers['Content-Type'] = 'application/json'
    r = requests.post(base_url+'users.getProfile', headers=headers)
    if r.status_code == 200:
        return json.loads(r.content.decode('utf8'))
    else :
        throw_this('Error: head() received response %s: %s' % (r.status_code,r.content.decode('utf8')) )
    return