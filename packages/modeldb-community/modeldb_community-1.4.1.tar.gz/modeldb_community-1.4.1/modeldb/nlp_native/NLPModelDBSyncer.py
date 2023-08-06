from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import make_scorer, mean_absolute_error, mean_squared_error
import  logging
import sys
import pandas as pd
from future.utils import with_metaclass
from sklearn.linear_model import *

from sklearn.calibration import *
from sklearn import  metrics
from modeldb.thrift.modeldb.ttypes import  ExperimentRun ,Project,Experiment
from modeldb.basic.Structs import (
            Model, ModelConfig, ModelMetrics, Dataset)
from sklearn.ensemble import *
from sklearn.pipeline import Pipeline
from modeldb.utils.Singleton import Singleton
from modeldb.basic import *
from modeldb.events import *
import  fasttext
import jieba
from gensim.models import word2vec
from modeldb.thrift.modeldb import  ttypes as modeldb_types
from modeldb.thrift.modeldb import  ModelDBService
# from ..basic import *
# from ..events import *
# from ..thrift.modeldb import ModelDBService
# from ..thrift.modeldb import ttypes as modeldb_types

from pymongo import MongoClient
import  gridfs
from bson.objectid import ObjectId
import  logging
import sklearn.metrics
from sklearn.externals import joblib
import sklearn, sklearn_pandas

import os
import re
from glob import glob
import pickle
# from ..events import FitEvent ,TransformEvent,PipelineEvent,GridSearchCVEvent,MetricEvent,RandomSplitEvent,ExperimentEvent

import numpy as np
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from keras.layers import Input,Dense, Activation, Embedding, LSTM
from keras.layers import Conv2D, MaxPooling2D, Flatten,TimeDistributed
from keras import backend as K
from keras.models import Sequential,Model
from keras.optimizers import SGD,Adagrad
import logging

logger=logging.getLogger(__name__)

def word2vec_fit_fn(self,dataset,size=20, window=5, min_count=5, workers=4):
    logger.info("fit model for keras")
    model = self.Word2Vec(dataset, size=size, window=window, min_count=min_count, workers=workers)
    meta_dict={ 'size':size,'window':window,'min_count':min_count,'workers':workers}
    fit_event=FitEvent(model,self,pd.DataFrame(),meta_dict)
    Syncer.instance.add_to_buffer(event=fit_event)
    return model

def fasttext_fit_fn(self,dataset,model_savepath,label_prefix='__label__', **params):
    model=fasttext.supervised(dataset,model_savepath,label_prefix=label_prefix)
    meta_dict={}
    if params ==None:
        params=meta_dict
    fit_event = FitEvent(model, self, pd.DataFrame(), params)
    Syncer.instance.add_to_buffer(event=fit_event)
    return model


# def  compile_fn(self,loss,optimizer,metrics):
#     logger.info("compile the model")
#
#     transform_event=TransformEvent()
#     Syncer.instance.add_to_buffer(event=transform_event)
#
#
# def  train_batch_fn(self,x_batch,y_batch):
#     logger.info("batch train the dataset")
#

def  predict_fn(self,x_test,batch_size=128):
    logger.info("predict use the model")

    predict_event=TransformEvent()
    Syncer.instance.add_to_buffer(event=predict_event)

def metrics_fn(self,metric_func):
    logger.info("metrics the model ")

    metric_event=MetricEvent()
    Syncer.instance.add_to_buffer(event=metric_event)
def convert_prediction_to_event(model, predict_array, x):
    predict_df = pd.DataFrame(predict_array)
    # Assign names to the predicted columns.
    # This is to ensure there are no merge conflicts when joining.
    num_pred_cols = predict_df.shape[1]
    pred_col_names = []
    for i in range(0, num_pred_cols):
        pred_col_names.append('pred_' + str(i))
    predict_df.columns = pred_col_names
    if not isinstance(x, pd.DataFrame):
        x_to_df = pd.DataFrame(x)
        new_df = x_to_df.join(predict_df)
    else:
        new_df = x.join(predict_df)
    predict_event = TransformEvent(x, new_df, model)
    Syncer.instance.add_to_buffer(predict_event)
    return predict_array



class Syncer(with_metaclass(Singleton, ModelDbSyncerBase.Syncer)):
    instance = None
    def __init__(self, project_config, experiment_config, experiment_run_config,
            thrift_config=None):
        self.enable_nlp_fn()
        self.local_id_to_path = {}
        Syncer.instance = self

        super(Syncer, self).__init__(project_config, experiment_config,experiment_run_config, thrift_config)

    def __str__(self):
        return  "nlp_syncer"

    def  enable_nlp_fn(self):
        setattr(word2vec,'fit_sync',word2vec_fit_fn)
        setattr(fasttext,'fit_sync',fasttext_fit_fn)
        from keras.models import Model,Sequential
        # for cls in [Model,Sequential]:
        #     setattr(cls,"fit_sync",fit_fn)
        #     setattr(cls,'compile_sync',compile_fn)
        #     setattr(cls,'predict_sync',predict_fn)
        #     setattr(cls,'metrics_sync',metrics_fn)