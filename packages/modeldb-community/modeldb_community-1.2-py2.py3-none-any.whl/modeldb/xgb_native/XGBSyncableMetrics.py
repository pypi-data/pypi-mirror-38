import numpy as np
import pandas as pd
from .XGBModelDBSyncer import Syncer

from sklearn.linear_model import *
from sklearn.preprocessing import *
from sklearn.pipeline import Pipeline

from sklearn import  metrics

from modeldb.basic import *
from modeldb.events import *

def compute_roc_auc_sync(model,test_y,y_pred,df,prediction_col='',label_col='',**params):
    roc_auc=metrics.roc_auc_score(test_y,y_pred)
    metrics_event=MetricEvent(df,model,label_col,prediction_col,metrics.roc_auc_score.__name__,roc_auc)
    Syncer.instance.add_to_buffer(metrics_event)
    print(Syncer.buffer_list)
    return roc_auc


def compute_accuracy_score_sync(model,test_y,y_pred,df,prediction_col,label_col,**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    accuracy_score=metrics.accuracy_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,model,label_col,prediction_col,metrics.accuracy_score.__name__,accuracy_score)
    Syncer.instance.add_to_buffer(metrics_event)
    return accuracy_score

def compute_recall_score_sync(model,test_y,y_pred,df,prediction_col,lable_col,**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    recall_score=metrics.recall_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,model,lable_col,prediction_col,metrics.recall_score.__name__,recall_score)
    Syncer.instance.add_to_buffer(metrics_event)
    return recall_score

def compute_precision_score_sync(model,test_y,y_pred,df,prediction_col='',lable_col='',**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    print("hello precision")
    precision_score=metrics.precision_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,model,lable_col,prediction_col,metrics.precision_score.__name__,precision_score)
    Syncer.instance.add_to_buffer(metrics_event)
    print(Syncer.buffer_list)
    return precision_score

def compute_f1_score_sync(model,test_y,y_pred,df,prediction_col,lable_col,**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    f1_score=metrics.f1_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,model,lable_col,prediction_col,metrics.f1_score.__name__,f1_score)
    Syncer.instance.add_to_buffer(metrics_event)
    return  f1_score

def compute_metrics_xgb_all_sync(
        model,  actual, predicted, df, prediction_col, label_col,
        **params):
    accuracy_score=compute_accuracy_score_sync(model,actual,predicted,df,prediction_col,label_col)
    roc_auc=compute_roc_auc_sync(model,actual,predicted,df,prediction_col,label_col)
    f1_score=compute_f1_score_sync(model,actual,predicted,df,prediction_col,label_col)
    precision_score=compute_precision_score_sync(model,actual,predicted,df,prediction_col,label_col)
    recall_score=compute_recall_score_sync(model,actual,predicted,df,prediction_col,label_col)
    score_map={"roc_auc":roc_auc,"accuracy_score":accuracy_score,"f1_score":f1_score,"precision_score":precision_score,"recall_score":recall_score}
    return  score_map

def compute_xgbmodel_feature_importance_sync(self,model,feature,df):
    feature_score = model.get_fscore()
    feature_score = sorted(feature_score.items(), key=lambda x: x[1], reverse=True)
    fscore = map()
    for (key, value) in feature_score:
        fscore[key]=value

    fit_event=FitEvent(model,feature,df,fscore)
    Syncer.instance.add_to_buffer(fit_event)
    return  fscore