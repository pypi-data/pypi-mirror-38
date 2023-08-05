#!/usr/bin/env python3

from __future__ import print_function, unicode_literals

import os
import json
import sys
from .table import Table
from .util import authentication, throw_this, print_this
from .api_requests import api_requests


class CountAPI:
    """CountAPI class. Contains the following methods:
    - set_api_token(str: api_token):
          Sets API token obtained from count.co.
    - upload(str: path = None, str: name = None, str: data = None, str: overwrite_key = None):
          Uploads csv file from path or csv data from str (keyword arg only method).
          Returns Table object.
    - delete_table(str: table_key):
          Deletes specified table from count.co server.
    - table(str: table_key):
          Get a table object from an existing table key. Returns Table Object.
    """
    def __init__(self):
        self.headers = None

    def set_api_token(self, api_token):
        """CountAPI.set_api_token(str: api_token)
           Sets API token obtained from count.co.
        """
        self.headers = {'Authorization':  'Bearer %s' % (api_token)}

    @authentication
    def upload(self, *args, **kwargs):
        """CountAPI.upload(str: path, str: name, str: overwrite_key, str: append_key, str: data)
           Uploads csv file from path or csv data from str (keyword arg only method).
           Returns Table object.
        """

        # CountAPI.upload(str: path, str: name, str: overwrite_key, str: append_key, str: data, list of str: column_types, list of str: column_names)

        path = kwargs.pop('path') if 'path' in kwargs else None
        name = kwargs.pop('name') if 'name' in kwargs else None
        overwrite_key = kwargs.pop('overwrite_key') if 'overwrite_key' in kwargs else None
        append_key = kwargs.pop('append_key') if 'append_key' in kwargs else None
        data = kwargs.pop('data') if 'data' in kwargs else None
        types = kwargs.pop('column_types') if 'column_types' in kwargs else None
        names = kwargs.pop('column_names') if 'column_names' in kwargs else None

        # Check raw dataframe not uploaded
        if 'pandas.core.frame.DataFrame' in str(type(data)):
            throw_this('Error: cannot upload raw dataframe; please use DataFrame.to_csv() function.')
        if kwargs:
            throw_this('Error: unexpected **kwargs: %s' % (list(kwargs.keys())) )
        if args:
            throw_this('Error: upload function expects keyword arguments only.')
        if path and data:
            throw_this('Error: either path or data must be specified, but not both')
        if overwrite_key and append_key:
            throw_this('Error: both overwrite_key and append_key cannot be specified')
        if types and not isinstance(types,list):
            throw_this('Error: column_types must be a list of strings')
        if names and not isinstance(names,list):
            throw_this('Error: column_names must be a list of strings')

        if append_key:
            number_of_cols = api_requests.tables_getmetadata(self.headers, append_key)[0]
            if types and len(types) != number_of_cols:
                throw_this('Error: Length column_types list does not match number of colums in table: %s' % (number_of_cols))
            if names and len(names) != number_of_cols:
                throw_this('Error: Length column_names list does not match number of colums in table: %s' % (number_of_cols))

        acceptable_types = ['string', 'int', 'double', 'datetime']
        if types:
            types = [t.lower() for t in types]
            for type_ in types:
                if type_ not in acceptable_types:
                    throw_this('Error: %s is not an acceptable column type. Acceptable column types are %s' % (type_, acceptable_types))

        # Check table exists
        if overwrite_key:
            if not isinstance(overwrite_key,str) or len(overwrite_key) != 11:
                throw_this('Error: expected 11 character alphanumeric strings for key.')
            try:
                api_requests.tables_getmetadata(self.headers, overwrite_key)
            except:
                throw_this('Error: table corresponding to overwrite_key %s not found' % (overwrite_key))

        r = None
        if path:
            if os.path.isfile(path):
                r = api_requests.tables_upload_file(self.headers, path, name, overwrite_key=overwrite_key, append_key=append_key, column_types=types, column_names=names)
            else: 
                throw_this('Error: cannot find: ' + path)
        if data:
            if len(data) > 0:
                r = api_requests.tables_upload_data(self.headers, data, name, overwrite_key=overwrite_key, append_key=append_key, column_types=types, column_names=names)
            else :
                throw_this('Error: data length 0')
        return Table(r, self)

    @authentication
    def delete_table(self, table_key):
        """CountAPI.delete_table(str: table_key)
           Deletes specified table from count.co server.
        """
        api_requests.tables_delete(self.headers, table_key)
        return

    def table(self, table_key):
        """CountAPI.table(str: table_key)
           Get a table object from an existing table key.
           Returns Table Object.
        """
        return Table(table_key, self)

    @authentication
    def _get_notebook_metadata(self, notebook_key):
        return api_requests.tables_getnotebook_metadata(self.headers, notebook_key)