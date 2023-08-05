#!/usr/bin/env python3

from __future__ import print_function, unicode_literals

import requests
import os
import json
import sys
from datetime import datetime, timedelta

def throw_this(msg):
  raise Exception('CountAPI: ' + msg)

class Column:
    """Column class. Contains the following methods:
    - aggregate(str: aggregate):
          Add aggregate function to Column object.
          Available aggregates are:
              str: ['DISTINCT', 'MIN', 'MAX', 'MED']
              other: ['DISTINCT', 'MIN', 'MAX', 'MED', 'SUM', 'AVG', 'STD', 'VAR', 'MED']
          Note: cannot perform both group_by and aggregate on the same Column object 
          Returns self.
    - group_by(str: grouping):
           Add grouping function to Column object.
           Available groupings are:
              str: []
              number: ['AUTO']
              datetime: ['YEAR', 'MONTH', 'WEEK', 'DAY', 'HOUR', 'MINUTE', 'SECOND']
           Note: cannot perform both group_by and aggregate on the same Column object 
           Returns self.
    - filter(str: comparator, str or int or float or datetime: value):
           Get Filter object from Column object with specified comparator and value.
           Available comparators are:
              str: ['IN']
              other : ['>', '>=', '<', '<=']
          Returns Filter object.
    - filter_list(list of tuples: filter_list):
          Get Filter object from Column object with list of filter tuples - (str: comparator, str or int or float or datetime: value)
          Available comparators are:
              str: ['IN']
              other : ['>', '>=', '<', '<=']
          Returns Filter object.
    """
    def __init__(self, key, type, name, operator = None):
        self.key = key
        self.type = type
        self.name = name
        self.operator = operator
        self.grouping = None
    
    def aggregate(self, aggregate):
        """Column.aggregate(str: aggregate):
           Add aggregate function to Column object.
           Available aggregates are:
              str: ['DISTINCT', 'MIN', 'MAX', 'MED']
              other: ['DISTINCT', 'MIN', 'MAX', 'MED', 'SUM', 'AVG', 'STD', 'VAR', 'MED']
           Note: cannot perform both group_by and aggregate on the same Column object 
           Returns self.
        """
        if self.grouping:
          msg = 'Error: a Column object cannot have a grouping and an aggregate'
          throw_this(msg)
        available_aggregates = []
        if self.type == 'string':
            available_aggregates = ['DISTINCT', 'MIN', 'MAX']
        else:
            available_aggregates = ['DISTINCT', 'MIN', 'MAX', 'MED', 'SUM', 'AVG', 'MED', 'NUMBER OF RECORDS']
        if aggregate.upper() in available_aggregates:
            self.operator = aggregate.upper()
        else:
            msg = '''Error: aggregate {aggregate} not allowed for a column of type {type}. List of available aggregates for {type} is [{list}]'''.format(type=self.type, list=','.join(available_aggregates), aggregate=aggregate)
            throw_this(msg)
        return self

    def group_by(self, grouping):
        """Column.group_by(str: grouping):
           Add grouping function to Column object.
           Available groupings are:
              str: []
              number: ['AUTO']
              datetime: ['YEAR', 'MONTH', 'WEEK', 'DAY', 'HOUR', 'MINUTE', 'SECOND']
           Note: cannot perform both group_by and aggregate on the same Column object 
           Returns self.
        """
        if self.operator:
          msg = 'Error: a Column object cannot have a grouping and an aggregate'
          throw_this(msg)
        available_groupings = []
        if self.type == 'string':
            available_groupings = []
        elif self.type == 'datetime':
            available_groupings = ['YEAR', 'MONTH', 'WEEK', 'DAY', 'HOUR', 'MINUTE', 'SECOND']
        else:
            available_groupings = ['AUTO']
        if grouping.upper() in available_groupings:
            self.grouping = grouping.upper()
        else:
            msg = '''Error: grouping {grouping} not allowed for a column of type {type}. List of available groupings for {type} is [{list}]'''.format(type=self.type, list=','.join(available_groupings), grouping=grouping)
            throw_this(msg)
        return self

    def filter(self, comparator, value):
        """Column.filter(str: comparator, str or int or float or datetime: value):
           Get Filter object from Column object with specified comparator and value.
           Available comparators are:
              str: ['IN']
              other : ['>', '>=', '<', '<=']
           Returns Filter object.
        """
        return Filter(key=self.key,type=self.type,name=self.name).filter(comparator, value)

    def filter_list(self, filter_list):
        """Column.filter_list(list of tuples: filter_list):
           Get Filter object from Column object with list of filter tuples - (str: comparator, str or int or float or datetime: value)
           Available comparators are:
              str: ['IN']
              other : ['>', '>=', '<', '<=']
           Returns Filter object.
        """
        return Filter(key=self.key,type=self.type,name=self.name).filter_list(filter_list)

class Filter:
    """Filter class. Contains the following methods:
    - filter(str: comparator, str or int or float or datetime: value):
           Add filter to this Filter object with specified comparator and value.
           Available comparators are:
              str: ['IN']
              other : ['>', '>=', '<', '<=']
          Returns self.
    - filter_list(list of tuples: filter_list):
          Add filters to this Filter object - expects list of tuples of form (str: comparator, str or int or float or datetime: value)
          Available comparators are:
              str: ['IN']
              other : ['>', '>=', '<', '<=']
          Returns self.
    """
    def __init__(self, key, type, name, comparator = None, value = None, negate = False):
        self.key = key
        self.type = type
        self.name = name
        self.comparator_value = [{'comparator': comparator, 'value': value, 'negate': False}] if comparator and value else []

    def filter(self, comparator, value):
        """Filter.filter(str: comparator, str or int or float or datetime: value):
           Add filter to this Filter object with specified comparator and value.
           Available comparators are:
              str: ['IN']
              other : ['>', '>=', '<', '<=']
          Returns self.
        """
        filter_list = []
        if 'IN' in comparator and type(value) is list:
            for v in value:
                filter_list.append((comparator, v))
        else:
            filter_list.append((comparator, value))
        return self.filter_list(filter_list)

    def filter_list(self, filter_list):
        """Filter.filter_list(list of tuples: filter_list):
           Add filters to this Filter object - (str: comparator, str or int or float or datetime: value)
           Available comparators are:
              str: ['IN']
              other : ['>', '>=', '<', '<=']
           Returns self.
        """
        available_comparators = []
        if self.type == 'string':
            available_comparators = ['IN', 'NOT IN']
        else:
            available_comparators = ['>', '>=', '<', '<=', '=', '!=']
        
        for c, val in filter_list:
            comparator = c
            value = val
            if comparator.upper() not in available_comparators:
                msg = 'Error: comparator {comparator} not allowed for a column of type {type}. List of available comparators for {type} is [{list}]'.format(type=self.type, list=','.join(available_comparators), comparator=comparator)
                throw_this(msg)
                return self

            if isinstance(value,tuple) and self.type != 'datetime':
                throw_this('Error: tuple can only be used on datetime type Column.')
                return self
            if isinstance(value,datetime) and self.type != 'datetime':
                throw_this('Error: datetime can only be used on datetime type Column.')
                return self

            negate = False
            if comparator == 'NOT IN':
                negate = True
                comparator = 'IN'
            if comparator == '!=':
                negate = True
                comparator = '='

            if self.type == 'datetime':
                if isinstance(value,datetime):
                    v = int((value - datetime(1970,1,1)).total_seconds()*1000)
                    self.comparator_value.append({'comparator': comparator, 'value': v, 'negate': negate})
                elif isinstance(value,list) or isinstance(value,tuple):
                    v = list(value)
                    y,m,d = (0,0,0)
                    if len(v) == 1:
                        y, = v
                    elif len(v) == 2: 
                        y,m, = v
                    else:
                        y,m,d, = v[:3]
                        
                    v = int((datetime(y,max(m,1),max(d,1)) - datetime(1970,1,1)).total_seconds()*1000)
                    if comparator == '=':
                        self.comparator_value.append({'comparator': '>=', 'value': v, 'negate': negate})
                        if d:
                            upper = datetime(y,max(m,1),d+1)
                        elif m:
                            upper = datetime(y,m+1,d)
                        else:
                            upper = datetime(y+1,max(m,1),max(d,1))
                        upper = int((upper - datetime(1970,1,1)).total_seconds()*1000) - 1
                        self.comparator_value.append({'comparator': '<', 'value': upper, 'negate': negate})
                    else:
                        self.comparator_value.append({'comparator': comparator, 'value': v, 'negate': negate})
                else:
                    self.comparator_value.append({'comparator': comparator, 'value': value, 'negate': negate})
            else:
                if comparator == '=':
                    self.comparator_value.append({'comparator': '>=', 'value': value, 'negate': negate})
                    delta = 1 if self.type == 'int' else 1e-10
                    self.comparator_value.append({'comparator': '<', 'value': value + delta, 'negate': negate})
                else:
                    self.comparator_value.append({'comparator': comparator, 'value': value, 'negate': negate})

        if len([cv for cv in self.comparator_value if cv['negate']])>0 and len([cv for cv in self.comparator_value if not cv['negate']])>0:
            throw_this('Error: cannot combine both IN/= and NOT IN/!= filters')
        if len([cv for cv in self.comparator_value if cv['comparator'] == '=']) and len([cv for cv in self.comparator_value if not cv['comparator'] != '='])>0:
            throw_this('Error: cannot combine =/!= with other filters')
        return self