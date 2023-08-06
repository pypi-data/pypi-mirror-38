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


from pyspark.sql import Row
from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import LogisticRegression,LinearSVCModel,LogisticRegressionModel,DecisionTreeClassificationModel,DecisionTreeRegressionModel,NaiveBayesModel,GBTClassificationModel,RandomForestClassificationModel,TreeEnsembleModel

import logging

logger=logging.getLogger(__name__)

def fit_fn(self,x_train,y_train,epochs=5,batch_size=32,**params):
    logger.info("fit model for keras")
    model=self.fit(x_train,y_train,params)
    fit_event = FitEvent(model, self, x_train, params)
    Syncer.instance.add_to_buffer(event=fit_event)
    return


def  compile_fn(self,loss,optimizer,metrics):
    logger.info("compile the model")

    # transform_event=TransformEvent()
    # Syncer.instance.add_to_buffer(event=transform_event)



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

def  predict_fn(self,x_test,batch_size=128,**params):
    logger.info("predict use the model")
    predict_array = self.transform(x_test, params)
    return convert_prediction_to_event(self, predict_array, x_test)


def compute_roc_auc_sync(self,test_y,y_pred,df,prediction_col='',label_col='',**params):
    roc_auc=metrics.roc_auc_score(test_y,y_pred)
    print("compute is "+ str(roc_auc))
    metrics_event=MetricEvent(df,self,label_col,prediction_col,metrics.roc_auc_score.__name__,roc_auc)
    Syncer.instance.add_to_buffer(metrics_event)

    return roc_auc

def compute_mean_absolute_error(self,test_y,y_pred,df,prediction_col='',label_col='',**params):
    mae=mean_absolute_error(test_y,y_pred=y_pred)
    print("compute is "+ str(mae))
    metrics_event=MetricEvent(df,self,label_col,prediction_col,mean_absolute_error.__name__,mae)
    Syncer.instance.add_to_buffer(metrics_event)
    return mae

def  compute_mean_squared_error(self,test_y,y_pred,df,prediction_col='',label_col='',**params):
    mse=mean_squared_error(test_y,y_pred=y_pred)
    metrics_event=MetricEvent(df,self,label_col,prediction_col,mean_squared_error.__name__,mse)
    Syncer.instance.add_to_buffer(metrics_event)
    return mse


def compute_accuracy_score_sync(self,test_y,y_pred,df,prediction_col='',label_col='',**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    accuracy_score=metrics.accuracy_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,self,label_col,prediction_col,metrics.accuracy_score.__name__,accuracy_score)
    Syncer.instance.add_to_buffer(metrics_event)
    return accuracy_score

def compute_recall_score_sync(self,test_y,y_pred,df,prediction_col='',lable_col='',**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    recall_score=metrics.recall_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,self,lable_col,prediction_col,metrics.recall_score.__name__,recall_score)
    Syncer.instance.add_to_buffer(metrics_event)
    return recall_score

def compute_precision_score_sync(self,test_y,y_pred,df,prediction_col='',lable_col='',**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    print("hello precision")
    precision_score=metrics.precision_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,self,lable_col,prediction_col,metrics.precision_score.__name__,precision_score)
    Syncer.instance.add_to_buffer(metrics_event)
    print(Syncer.buffer_list)
    return precision_score

def compute_f1_score_sync(self,test_y,y_pred,df,prediction_col='',lable_col='',**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    f1_score=metrics.f1_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,self,lable_col,prediction_col,metrics.f1_score.__name__,f1_score)
    Syncer.instance.add_to_buffer(metrics_event)
    return  f1_score

switch={
    'roc_auc':compute_accuracy_score_sync,
    'f1_score':compute_f1_score_sync,
    'precision_score':compute_precision_score_sync,
    'recall_score':compute_recall_score_sync,
    'accuracy_score':compute_accuracy_score_sync,
    'mean_squared_error':compute_mean_squared_error,
    'mean_absolute_error':compute_mean_absolute_error
}
def metrics_fn(self,metric_func, test_y, y_pred, df, prediction_col='', label_col='', **params):
    logger.info("metrics the model ")
    try:
        score= switch[metric_func](self,test_y,y_pred,df,prediction_col,label_col)
        return score
    except KeyError as e:
        logger.error(str(e))
        pass

def metrics_fn(self,metric_func):
    logger.info("metrics the model ")

    metric_event=MetricEvent()
    Syncer.instance.add_to_buffer(event=metric_event)



class Syncer(with_metaclass(Singleton, ModelDbSyncerBase.Syncer)):
    instance = None
    def __init__(self, project_config, experiment_config, experiment_run_config,
            thrift_config=None):
        self.enable_pyspark_fn()
        self.local_id_to_path = {}
        Syncer.instance = self

        super(Syncer, self).__init__(project_config, experiment_config,experiment_run_config, thrift_config)

    def __str__(self):
        return  "pyspark_syncer"

    def  enable_pyspark_fn(self):
        from keras.models import Model,Sequential
        for cls in [Model,Sequential]:
            setattr(cls,"fit_sync",fit_fn)
            setattr(cls,'compile_sync',compile_fn)
            setattr(cls,'predict_sync',predict_fn)
            setattr(cls,'metrics_sync',metrics_fn)