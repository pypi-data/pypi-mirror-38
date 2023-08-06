# !/usr/bin/env python
# coding: utf-8
import click
import tempfile, os
from sklearn.externals import joblib
from MachineLearningForTextcategory.data import DataSet, PredictionDateSet, lableInFileDateSet
from MachineLearningForTextcategory.model import SVC_Model
from MachineLearningForTextcategory.logger import LOG


@click.group()
def cli():
    click.echo('smart machine learning')

@cli.command()
@click.option('--train_path', help='the train resource datas full path.')
@click.option('--model_save_path', default="train.pkl", help='the train model save path.')
def train(train_path, model_save_path):
    train_datas = DataSet(train_path)
    train_model = SVC_Model(train_datas.data, train_datas.category_ids, train_datas.category_names)
    train_model.build_with_category_names(model_save_path)

@cli.command()
@click.option('--file_path', help='the train resource file which every line include feature and lable.')
@click.option('--model_save_path', default="train.pkl", help='the train model save path.')
def train_model_from_file(file_path, model_save_path):
    train_datas = lableInFileDateSet(file_path)
    train_model = SVC_Model(train_datas.data, train_datas.category_ids, train_datas.category_names)
    train_model.build_with_category_names(model_save_path)
 
@cli.command()
@click.option('--file_path', required=False, help='the prdict datas full path.')
@click.option('--model_path', required=True, help='the useable model path.')
@click.option('--predict_words', required=False, help='the string datas which need predict.')
def predict(file_path, model_path, predict_words=None):
    if predict_words:
        docs_test = [predict_words]
        test_file_names = docs_test
    else:
        test_datas = PredictionDateSet(file_path)
        docs_test = test_datas.data
        test_file_names = test_datas.file_names
    text_clf = joblib.load(model_path)
    predicted_type_index = text_clf.predict(docs_test)
    LOG.info(predicted_type_index)
    predict_proba = text_clf.predict_proba(docs_test)
    test_amounts = predict_proba.shape[0]
    #threshold = 0.6
    for i in range(test_amounts):
        every_proba = predict_proba[i].tolist()
        max_proba = max(every_proba)
        max_proba_index = every_proba.index(max_proba)
        # file_name = test.filenames[i].split('/')
        # if every_proba[max_proba_index] > threshold: # output probability more than threshold
        # print '111111111', every_proba[max_proba_index], predicted_type_index[i]
        LOG.info("label and proba:{} {}".format(text_clf.classes_, predict_proba[i]))
        LOG.info('predict detail:{} {}'.format(test_file_names[i], zip(text_clf.classes_, predict_proba[i])))
        print '\n\n'


if __name__ == "__main__":
    cli()
