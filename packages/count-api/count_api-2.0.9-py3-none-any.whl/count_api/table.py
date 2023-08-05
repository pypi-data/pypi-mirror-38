#!/usr/bin/env python3

from __future__ import print_function, unicode_literals, absolute_import

import os
import json
from .table_tile import TableTile
from .util import print_this, throw_this, authentication, base_url, base_return_url
from .visual import ChartOptions, Visual
from .column import Column, Filter
from .api_requests import api_requests

class Table:
    """Table class. Contains the following methods:
    - [int: index]:
          Get Column object from column index.
          Returns Column Object.
    - [str: name]:
          Get Column object from column name. Returns first column found with header matching name.
          Returns Column Object.
    - column(int: index):
          Get Column object from column index.
          Returns Column Object.
    - column(str: name):
          Get Column object from column name. Returns first column found with header matching name.
          Returns Column Object.
    - columns(str: name = None):
          Get list of Column objects with headers matching name parameter.
          Returns list of Column Objects.
    - delete():
          Deletes table from count.co server.
          Future references to this Table will be undefined.
    - head(int: n=10):
          Prints first n rows of table
    - overwrite(str: path, str: name, str: data):
          Uploads csv file from path or csv data from str (keyword arg only method), overwriting existing table.
          Returns self.
    - size():
           Size of table as a tubple of ints (column_extent, row_extent)
           Returns tuple (int, int)
    - upload_visual(Column: x = None, Column: y = None, Column: color = None, Column: size = None, Filter or list of Filters: filters = None, dict: chart_options = None):
          Uploads chart visual to count.co.
          Returns Visual object.
    - url():
          Get url to table view on count.co.
          Returns str.
    """
    def __init__(self, table_key, count_api):
        self.headers = count_api.headers
        self.key = table_key

    def _get_most_restrictive_filters(self, filters):
        ret_filters = []
        string_filters = [f for f in filters if f['comparator'] == 'IN']
        # combine string filters
        filter_keys = [f['columnKey'] for f in string_filters if f['negate']]
        for filter_key in set(filter_keys):
            # assumes only one comparator IN
            values = []
            [values.append(f['value']) for f in string_filters if f['columnKey'] == filter_key]
            ret_filters.append({'columnKey':filter_key, 'columnType': 'string', 'comparator': 'IN', 'value': values, 'negate': True})

        filter_keys = [f['columnKey'] for f in string_filters if not f['negate']]
        for filter_key in set(filter_keys):
            # assumes only one comparator IN
            values = []
            [values.append(f['value']) for f in string_filters if f['columnKey'] == filter_key]
            ret_filters.append({'columnKey':filter_key, 'columnType': 'string', 'comparator': 'IN', 'value': values, 'negate': False})

        filter_keys = [f['columnKey'] for f in filters if f['comparator'] != 'IN']
        for filter_key in set(filter_keys):
            col_filters = [f for f in filters if f['columnKey'] == filter_key]
            gt = [f for f in col_filters if '>' in f['comparator']]
            if gt:
                hi = gt[0]
                for f in gt:
                    if f['value'] > hi['value']:
                        hi = f
                        continue
                    if f['value'] == hi['value'] and hi['comparator'] != '>':
                        hi = f
                ret_filters.append(hi)
            lt = [f for f in col_filters if '<' in f['comparator']]
            if lt:
                lo = lt[0]
                for f in lt:
                    if f['value'] < lo['value']:
                        lo = f
                        continue
                    if f['value'] == lo['value'] and lo['comparator'] != '<':
                        lo = f
                ret_filters.append(lo)
        return ret_filters

    def _fill_missing_filters(self, filters, column_data):
        filter_keys = [f['columnKey'] for f in filters if f['comparator'] == 'IN']
        ret_filters = [f for f in filters if f['columnKey'] in filter_keys]
        
        filter_keys = [f['columnKey'] for f in filters if f['comparator'] != 'IN']
        tmp_filters = [f for f in filters if f['columnKey'] in filter_keys]
        for col in [c for c in column_data if c['key'] in filter_keys]:
            col_filters = [f for f in filters if f['columnKey'] == col['key']]
            if not [f for f in col_filters if '>' in f['comparator']]:
                tmp_filters.append({'columnKey':col['key'], 'columnType': col['type'], 'comparator': '>=', 'value': col['range'][0], 'negate': False})
            if not [f for f in col_filters if '<' in f['comparator']]:
                tmp_filters.append({'columnKey':col['key'], 'columnType': col['type'], 'comparator': '<=', 'value': col['range'][1], 'negate': False})

        for f_key in set(filter_keys):
            this_key_filters = [f for f in tmp_filters if f['columnKey'] == f_key]
            if this_key_filters:
                [lower_bound_filter] = [f for f in tmp_filters if '>' in f['comparator']]
                [upper_bound_filter] = [f for f in tmp_filters if '<' in f['comparator']]

                [col_type_range] = [(col['type'],col['range']) for col in column_data if col['key']==f_key]
                if col_type_range[0] == 'datetime':
                    # delta = col_type_range[1][0][1] - col_type_range[1][0][0]
                    # if not isinstance(lower_bound_filter['value'],list):
                    #   val = lower_bound_filter['value']
                    #   lower_bound_filter['value'] = [val,(val - val%delta) + delta]
                    # if not isinstance(upper_bound_filter['value'],list):
                    #   val = upper_bound_filter['value']
                    #   upper_bound_filter['value'] = [(val - val%delta),val]
                    # BERW: check with Oli here ... which element of datetime value do I put
                    if isinstance(lower_bound_filter['value'],list):
                        val = lower_bound_filter['value'][0]
                        lower_bound_filter['value'] = val
                    if isinstance(upper_bound_filter['value'],list):
                        val = upper_bound_filter['value'][1]
                        upper_bound_filter['value'] = val

                negate = lower_bound_filter['negate']
                if not negate  and lower_bound_filter['value'] > upper_bound_filter['value']:
                    negate = True
                    (lower_bound_filter['value'],upper_bound_filter['value']) = (upper_bound_filter['value'],lower_bound_filter['value'])
                ret_filters.append({'columnKey':lower_bound_filter['columnKey'], 'columnType': lower_bound_filter['columnType'], 'comparator': 'BETWEEN', 'value': [lower_bound_filter['value'], upper_bound_filter['value']], 'negate': negate})
        return ret_filters        

    def _expand_filters(self, filters):
        expanded_filters = []
        for f in filters:
            if f.comparator_value:
                expanded_filters.extend([{'columnKey':f.key, 'columnType': f.type, 'comparator': cv['comparator'], 'value': cv['value'], 'negate': cv['negate']} for cv in f.comparator_value])
        return expanded_filters

    def _get_select_from_columns(self, columns):
        column_objs = []
        for col in [col for col in columns if col]:
            op = None
            if col.grouping:
                grouping_to_query_op = {'AUTO': 'BINS(DEFAULT_)'}
                op = grouping_to_query_op.get(col.grouping,col.grouping.lower())
            elif col.operator:
                op = col.operator
            column_objs.append({'columnKey':col.key, 'columnType': col.type, 'operator': op })
        # Hack for bethe returning aggs first
        # for col in [col for col in columns if col]:
        #     if not col.grouping or not col.operator:
        #         column_objs.append({'columnKey':col.key, 'columnType': col.type, 'operator': None })
        return column_objs
    
    def _validate_columns(self,validation_msg,*args):
        if [a for a in args if a and "class 'Column'" in str(type(a))]:
            validation_msg.push('x, y must be objects of type Column if not defaulted')
    
    def _validate_filters(self,validation_msg,*args):
        if [a for a in args if a and "class 'Filter'" in str(type(a))]:
            validation_msg.push('filters must be a list of Filter objects if not defaulted')

    def _validate_chart_options(self,validation_msg,*args):
        if not isinstance(args, dict):
            validation_msg.push('chart_options must be a dictionary if not defauted')

    @authentication
    def upload_visual(self, x = None, y = None,  color = None,  size = None, aggregates = None, groupings = None, filters = None, chart_options = None):
        """Table.upload_visual(Column: x = None, Column: y = None, Column: color = None, Column: r = None, Filter or list of Filters: filters = None, dict: chart_options = None):
           Uploads chart visual to count.co.
           Returns Visual object.
        """
        star_operators = ['NUMBER OF RECORDS', 'NUMBER']
        axis_mapping = {'x': x, 'y': y, 'size': size, 'color': color}
        if aggregates:
            for axis_key in axis_mapping:
                axis = axis_mapping[axis_key]
                if axis_key in aggregates:
                    if not isinstance(aggregates[axis_key],str):
                        throw_this('Error: expected aggregate type str.')
                    if aggregates[axis_key].upper() in star_operators:
                        if axis:
                            throw_this('Error: %s Column should be None for star aggregate %s.' % (axis_key, aggregates[axis_key]))
                        axis_mapping[axis_key] = Column(key='*', type=None, name=None, operator='COUNT')
                    if axis:
                        axis.aggregate(aggregates[axis_key])

        x = axis_mapping['x']
        y = axis_mapping['y']
        size = axis_mapping['size']
        color = axis_mapping['color']

        if groupings:
            if 'x' in groupings and x:
                x.group_by(groupings['x'])
            if 'y' in groupings and y:
                y.group_by(groupings['y'])
            if 'size' in groupings and size:
                size.group_by(groupings['size'])
            if 'color' in groupings and color:
                size.group_by(groupings['color'])

        validation_msg = []
        self._validate_columns(self,validation_msg,x,y,size,color)
        self._validate_filters(self,validation_msg,filters)
        if validation_msg:
            throw_this(','.join(validation_msg))

        selects = self._get_select_from_columns([x,y,size,color])
        if filters is None:
            my_filters = []
        else:
            # add missing filters
            filters_list = filters if type(filters) is list else [filters]
            column_data = self._get_raw_columns_data()
            my_filters = self._fill_missing_filters(self._get_most_restrictive_filters(self._expand_filters(filters_list)), column_data)
            #my_filters = self._get_most_restrictive_filters(self._expand_filters(filters_list))
        orderings = []

        if chart_options is None:
          chart_options = {}

        chart_axes = {}
        for idx,(axis,s) in enumerate(zip(ChartOptions.AXES,[x,y,size,color])):
            result_col_type = None
            if s:
                result_col_type = 'int' if s.type == 'string' and s.operator == 'DISTINCT' else s.type
            chart_axes[axis] = {'key': s.key, 'type': result_col_type, 'idx': str(idx)} if s else None

        idx = 0

        dict_selects = {'x': x, 'y': y, 'size': size, 'color': color }
        for axis in ChartOptions.AXES:
            s = dict_selects[axis]
            if s:
                chart_axes[axis]['idx'] = idx
                idx = idx + 1

        chart_options_obj = ChartOptions(chart_options, chart_axes)

        query = {'filters': my_filters, 'orderings':orderings, 'selects':selects, 'tableKey': self.key}
        notebook_key = api_requests.tables_addnotebook(self.headers, self.key, query)

        user_profile = api_requests.users_getprofile(self.headers)
        workspaces = user_profile['workspaces']
        slack_token = None
        w_idx = 0
        if workspaces:
            while slack_token == None and w_idx < len(workspaces): 
                try:
                    slack_token = api_requests.auth_getstate(self.headers, notebook_key, workspaces[w_idx])
                except:
                    pass
                w_idx = w_idx + 1
                
        return Visual(notebook_key, self.key, slack_token['state']).set_chart_options(chart_options_obj)

    @authentication
    def _get_raw_columns_data(self):
        return api_requests.tables_getcolumns(self.headers, self.key)

    @authentication
    def columns(self, name=None):
        """Table.columns(str: name = None):
           Get list of Column objects with headers matching name parameter.
           Returns list of Column Objects.
        """
        columns = self._get_raw_columns_data()
        return [Column(key=col['key'],type=col['type'],name=col['name']) for col in columns if not name or col['name'] == name]

    @authentication
    def column(self, index_or_name):
        """Table.column(str or int: index_or_name):
           Get Column object from column name (str) or column index (int).
           When using name, first column found with header matching name is returned.
           Returns Column Object or None.
        """
        if isinstance(index_or_name, str):
          return self._column_with_name(index_or_name)
        if isinstance(index_or_name, int):
          return self._column_with_index(index_or_name)
        throw_this('Error: expected either string or integer')

    def __getitem__(self, index_or_name):
        """Table.column[str or int: index_or_name]:
           Get Column object from column name (str) or column index (int).
           When using name, first column found with header matching name is returned.
           Returns Column Object or None.
        """
        return self.column(index_or_name)

    def _column_with_name(self,name):
        columns = self.columns(name)
        if columns:
            return columns[0]
        return None

    def _column_with_index(self, index):
        columns = self.columns()
        if index < len(columns) and index > -1:
            return columns[index]
        return None

    @authentication
    def size(self):
        """Table.size()
           Size of table as a tubple of ints (column_extent, row_extent)
           Returns tuple (int, int)
        """
        ret = api_requests.tables_getmetadata(self.headers, self.key)
        return (ret[0], ret[1])

    @authentication
    def head(self, n=10):
        """Table.head(int: n=10)
           Prints first n rows of table
        """
        return self._head(n, 0)

    # @authentication
    # def tail(self, n=10):
    #     """Table.tail(n=10)
    #        Size of last n rows of table
    #     """
    #     end_at = self.size()[1]
    #     return self._head(n, end_at)

    def _head(self, n, end_at = None):
        limit = min(n,100)
        selects = [{'columnKey':'*', 'columnType': None, 'operator': None }]
        query = {'filters': [], 'orderings':[], 'selects':selects, 'tableKey': self.key}
        offset = 0
        r = api_requests.tables_getdata(self.headers, self.key, query, offset, end_at if end_at else limit)
        table_tile = TableTile(r)
        col_data = []
        col_names = []
        for col in table_tile.columns:
            col_data.append(col.slice_(0,limit))
            col_names.append(col.name)

        output = []
        row_output = ["{0:>6}".format('index')]
        for col in col_names:
            row_output.append("{0:>15}".format(str(col)[:12]))
        output.append(''.join(row_output))

        for i in range(0,limit):
            row_output = ["{0:>6}".format(str(i))]
            for col in col_data:
                row_output.append("{0:>15}".format(str(col[i])[:12]))
            output.append(''.join(row_output))
        print('\n'.join(output)) 


    @authentication
    def delete(self):
        """Table.delete()
           Deletes table from count.co server.
           Future references to this Table will be undefined.
        """
        api_requests.tables_delete(self.headers, self.key)
        return

    @authentication
    def overwrite(self, *args, **kwargs):
        """Table.overwrite(str: path, str: name, str: data)
           Upload csv file from path or csv data from str (keyword arg only method), overwriting existing table.
           column_types: acceptable types of column type are 'string', 'int', 'double', and 'datetime'.
           Returns self.
        """

        # Table.overwrite(str: path, str: name, str: data, list of str: column_types, list of str: column_names)

        path = kwargs.pop('path') if 'path' in kwargs else None
        name = kwargs.pop('name') if 'name' in kwargs else None
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
        if types and not isinstance(types,list):
            throw_this('Error: column_types must be a list of strings')
        if names and not isinstance(names,list):
            throw_this('Error: column_names must be a list of strings')

        acceptable_types = ['string', 'int', 'double', 'datetime']
        if types:
            types = [t.lower() for t in types]
            for type_ in types:
                if type_ not in acceptable_types:
                    throw_this('Error: %s is not an acceptable column type. Acceptable column types are %s' % (type_, acceptable_types))

        r = None
        if path:
            if os.path.isfile(path):
                r = api_requests.tables_upload_file(self.headers, path, name, overwrite_key=self.key, column_types=types, column_names=names)
            else: 
                throw_this('Error: cannot find: ' + path)
        if data:
            if len(data) > 0:
                r = api_requests.tables_upload_data(self.headers, data, name, overwrite_key=self.key, column_types=types, column_names=names)
            else :
                throw_this('Error: data length 0')

        self.key = r
        return self

    # @authentication
    # def append(self, *args, **kwargs):
    #     """Table.overwrite(str: path, str: name, str: data, list of str: column_types, list of str: column_names)
    #        Upload csv file from path or csv data from str (keyword arg only method), overwriting existing table.
    #        For column_types and column_names, length of lists must match number of columns in existing table.
    #        column_types: acceptable types of column type are 'string', 'int', 'double', and 'datetime'.
    #        Returns self.
    #     """
    #     path = kwargs.pop('path') if 'path' in kwargs else None
    #     name = kwargs.pop('name') if 'name' in kwargs else None
    #     data = kwargs.pop('data') if 'data' in kwargs else None
    #     types = kwargs.pop('column_types') if 'column_types' in kwargs else None
    #     names = kwargs.pop('column_names') if 'column_names' in kwargs else None

    #     # Check raw dataframe not uploaded
    #     if 'pandas.core.frame.DataFrame' in str(type(data)):
    #         throw_this('Error: cannot upload raw dataframe; please use DataFrame.to_csv() function.')

    #     if kwargs:
    #         throw_this('Error: unexpected **kwargs: %s' % (list(kwargs.keys())) )
    #     if args:
    #         throw_this('Error: upload function expects keyword arguments only.')
    #     if path and data:
    #         throw_this('Error: either path or data must be specified, but not both')
    #     if types and not isinstance(types,list):
    #         throw_this('Error: column_types must be a list of strings')
    #     if names and not isinstance(names,list):
    #         throw_this('Error: column_names must be a list of strings')

    #     number_of_cols = self.size()[0]
        
    #     if types and len(types) != number_of_cols:
    #         throw_this('Error: Length column_types list does not match number of colums in table: %s' % (number_of_cols))
    #     if names and len(names) != number_of_cols:
    #         throw_this('Error: Length column_names list does not match number of colums in table: %s' % (number_of_cols))
            
    #     acceptable_types = ['string', 'int', 'double', 'datetime']
    #     if types:
    #         types = [t.lower() for t in types]
    #         for type_ in types:
    #             if type_ not in acceptable_types:
    #                 throw_this('Error: %s is not an acceptable column type. Acceptable column types are %s' % (type_, acceptable_types))

    #     r = None
    #     if path:
    #         if os.path.isfile(path):
    #             r = api_requests.tables_upload_file(self.headers, path, name, overwrite_key=None, append_key=self.key, column_types=types, column_names=names)
    #         else: 
    #             throw_this('Error: cannot find: ' + path)
    #     if data:
    #         if len(data) > 0:
    #             r = api_requests.tables_upload_data(self.headers, data, name, overwrite_key=None, append_key=self.key, column_types=types, column_names=names)
    #         else :
    #             throw_this('Error: data length 0')

    #     self.key = r
    #     return self

    def url(self):
        """Table.url()
           Get url to table view on count.co.
           Returns str.
        """
        return  "%s/%s" % (base_return_url,self.key)
