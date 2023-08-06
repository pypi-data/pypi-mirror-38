# !/usr/bin/env python
# coding: utf-8

from sklearn import datasets
import numpy as np
import os


class DataSet(object):

    def __init__(self, data_path):
        self._data_sets = datasets.load_files(data_path)
    
    @property
    def data(self):
        return self._data_sets.data

    @property
    def category_ids(self):
        return self._data_sets.target

    @property
    def category_names(self):
        return self._data_sets.target_names

    @property
    def file_names(self):
        return self._data_sets.filenames


class PredictionDateSet(DataSet):

    def __init__(self, data_path):
        if os.path.isdir(data_path):
            self._data_sets = datasets.load_files(data_path)
        elif os.path.isfile(data_path):
            self._data_sets = DataSetDict()
            self._parse_prediction_file(data_path)
    
    def _parse_prediction_file(self, file_path):
        self._data_sets.filenames = os.path.basename(file_path).split()
        with open(file_path, 'r') as f:
            self._data_sets.data = [f.read()]


class lableInFileDateSet(DataSet):

    def __init__(self, file_path, delimiter=','):
        self._delimiter = delimiter
        if os.path.isfile(file_path):
            self._data_sets = DataSetDict()
            self._parse_file(file_path)

    def _parse_file(self, file_path):
        self._data_sets.filenames = os.path.basename(file_path).split()
        f = np.loadtxt(file_path, 'S5', delimiter=self._delimiter, converters={0: lambda s: s.replace(' ', '_')} )
        self._data_sets.data = f[:,0]
        self._data_sets.target_names = f[:,1]


class DataSetDict(object):

    def __init__(self):
        self.data = ""
        self.filenames = ""
        self.target = None
        self.target_names = None

