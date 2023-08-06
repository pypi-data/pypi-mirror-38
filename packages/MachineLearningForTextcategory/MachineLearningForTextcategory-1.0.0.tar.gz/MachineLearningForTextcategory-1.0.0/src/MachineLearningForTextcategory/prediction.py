# !/usr/bin/env python
# coding: utf-8
import sys, re, os
from sklearn.externals import joblib
import numpy as np
import click
from data import DataSet, PredictionDateSet


class NewData(object):

    def __init__(self, data, model_path):
        self._data = data
        self._model_path = model_path
        self._text_clf = joblib.load(self._model_path)

    def predict_category(self):
        predicted = self._text_clf.predict(self._data)
        return predicted

    def predict_probability(self):
        predict_proba = self._text_clf.predict_proba(self._data)
        # every_proba = predict_proba[0].tolist()
        return zip(self._text_clf.classes_, predict_proba[0])

    def output_result(self):
        pass


# @click.command()
# @click.option('--file_path', required=False, help='the prdict datas full path.')
# @click.option('--model_path', required=True, help='the useable model path.')
# @click.option('--predict_words', required=False, help='the string datas which need predict.')
# def predict_result(file_path, model_path, predict_words=None):
#     if predict_words:
#         docs_test = [predict_words]
#         test_file_names = docs_test
#     else:
#         test_datas = PredictionDateSet(file_path)
#         docs_test = test_datas.data
#         test_file_names = test_datas.file_names
#     text_clf = joblib.load(model_path)
#     predicted_type_index = text_clf.predict(docs_test)
#     predict_proba = text_clf.predict_proba(docs_test)
#     test_amounts = predict_proba.shape[0]
#     #threshold = 0.6
#     for i in range(test_amounts):
#         every_proba = predict_proba[i].tolist()
#         max_proba = max(every_proba)
#         max_proba_index = every_proba.index(max_proba)
#         # file_name = test.filenames[i].split('/')
#         # if every_proba[max_proba_index] > threshold: # output probability more than threshold
#         # print '111111111', every_proba[max_proba_index], predicted_type_index[i]
#         print 'predict detail:', test_file_names[i], zip(text_clf.classes_, predict_proba[i])
#         print '\n\n'


# if __name__ == "__main__":
#     predict_result()
#     # data = ["bts_debug_on\nSet_Mac_Log_Level\nSet MAC LOG LEVEL failed!"]
#     # test_dat = NewData(data, 'text_clf.ml')
#     # print test_dat.predict_probability()