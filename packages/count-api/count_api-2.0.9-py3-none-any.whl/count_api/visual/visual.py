#!/usr/bin/env python3

from __future__ import print_function, unicode_literals
from ..util import base_embed_url, base_preview_url, base_return_url

def throw_this(msg):
  raise Exception('CountAPI: ' + msg)

def print_this(msg):
  print('CountAPI: ' + msg)

class IFrame(object):
    """
    Generic class to embed an iframe in an IPython notebook
    """

    iframe = """
        <iframe
            width="{width}"
            height="{height}"
            src="{src}{params}"
            frameborder="0"
            allowfullscreen
        ></iframe>
        """

    def __init__(self, src, width, height):
        self.src = src
        self.width = width
        self.height = height

    def _repr_html_(self):
        """return the embed iframe"""
        params = ""
        return self.iframe.format(src=self.src,
                                  width=self.width,
                                  height=self.height,
                                  params=params)

class Visual:
    """Visual class. Contains the following methods:
    - embed():
          Returns IFrame to current visual.
          Returns IFrame.
    - set_chart_options(dict: chart_option):
          Set chart options.
          Returns self.
    - preview_url():
          Get url to preview view on count.co.
          Returns str.
    - url():
          Get url to visual view on count.co.
          Returns str.
    - url_embed():
           Get url to visual view on count.co suitable for embedding
           Returns str.
    """
    def __init__(self, key, table_key, slack_token = None):
        self.key = key
        self.table_key = table_key
        self.chart_options = None
        self.slack_token = slack_token

    def set_chart_options(self, chart_options):
        self.chart_options = chart_options
        return self

    def url(self):
        """Visual.url():
           Get url to visual view on count.co.
           Returns str.
        """
        return self._url(base_return_url)

    def url_embed(self):
        """Visual.url_embed():
           Get url to visual view on count.co suitable for embedding.
           Returns str.
        """
        return self._url(base_embed_url)

    def embed(self):
        """Visual.embed():
           Returns IFrame to current visual.
           Returns IFrame.
        """
        return IFrame(self.url_embed(),width = 1000,height = 1000)

    def _url(self, base_url):
        options_dict = self.chart_options.options_dict
        query_params = []
        query_params.append('v=%s' % (self.key))
        query_params.append('view=visual')
        query_params.extend(["%s=%s" % (key, options_dict[key]) for key in options_dict if options_dict[key]])
        return "%s/%s?%s" % (base_url,self.table_key,'&'.join(query_params))

    def preview_url(self):
        """Visual.preview_url():
           Get url to preview view on count.co.
           Returns str.
        """
        preview_url = self._url(base_preview_url)
        return "%s&state=%s" % (preview_url,self.slack_token)

class ChartOptions:
    AVAILABLE_AXIS_TYPES = ['linear', 'log']
    AVAILABLE_CHART_TYPES = ['circle', 'line', 'bar', 'area', 'auto']
    AXIS_TYPE_KEYS = ['x_type', 'y_type', 'size_type', 'color_type']
    AXIS_TYPE_MAPPING = {'x': 'x_type', 'y': 'y_type', 'size': 'size_type', 'color': 'color_type'}
    AXES = ['x', 'y', 'size', 'color']

    def __init__(self, chart_options, chart_axes):
        self.options_dict = {}
        self.chart_axes = chart_axes
        self.set_chart_options(chart_options)

    def validate_chart_options(self, chart_options):
        validation_msg = []

        if not isinstance(chart_options, dict):
            validation_msg.append('Error: expected dict type for chart_options')

        chart_axes = self.chart_axes
        if chart_options and isinstance(chart_options, dict):

            chart_type = chart_options.get('type', '').lower()
            if chart_type and chart_type not in ChartOptions.AVAILABLE_CHART_TYPES:
                validation_msg.append('Error: Chart type {chart_type} is not recognized. List of available chart types is [{list}]'.format(list=','.join(ChartOptions.AVAILABLE_CHART_TYPES), chart_type=chart_type))
            
            for axis_type_key in ChartOptions.AXIS_TYPE_KEYS:
                axis_type = chart_options.get(axis_type_key, '').lower()
                if axis_type and axis_type not in ChartOptions.AVAILABLE_AXIS_TYPES:
                    validation_msg.append('Error: {axis_type_key} {axis_type} is not recognized. List of available axis types is [{list}]'.format(list=','.join(ChartOptions.AVAILABLE_AXIS_TYPES), axis_type_key=axis_type_key, axis_type=axis_type))
            
            for axis,axis_type_key in zip(ChartOptions.AXES,ChartOptions.AXIS_TYPE_KEYS):
                if chart_axes[axis]:
                    if chart_options.get(axis_type_key, '').lower() and (chart_axes[axis]['type'] == 'string' or chart_axes[axis]['type'] == 'datetime'):
                        print_this('Warning: ignorning {axis_type_key} set for {type_} column'.format(axis_type_key=axis_type_key,type_=chart_axes[axis]['type']))
        return validation_msg

    def set_chart_options(self, chart_options):
        validation_msg = self.validate_chart_options(chart_options)
        if validation_msg:
            throw_this('|'.join(validation_msg))

        self.options_dict['type'] = chart_options.get('type', '').lower()
        if self.options_dict['type'] == 'auto':
          self.options_dict['type'] = None

        for axis_type_key in ChartOptions.AXIS_TYPE_KEYS:
            self.options_dict[axis_type_key] = None

        for axis,axis_type_key in zip(sorted(self.chart_axes),sorted(ChartOptions.AXIS_TYPE_KEYS)):
            if self.chart_axes[axis]:
                if self.chart_axes[axis]['type'] == 'string':
                    self.options_dict[axis_type_key] = 'ordinal'
                elif self.chart_axes[axis]['type'] == 'datetime':
                    self.options_dict[axis_type_key] = 'time'
                else:
                    self.options_dict[axis_type_key] = chart_options.get(axis_type_key, 'linear')
        
        for axis in self.chart_axes:
            if self.chart_axes[axis]:
                self.options_dict[axis] = str(self.chart_axes[axis]['idx'])

        return self