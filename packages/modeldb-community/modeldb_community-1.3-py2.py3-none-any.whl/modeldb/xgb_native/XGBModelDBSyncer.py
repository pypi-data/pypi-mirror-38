
from sklearn.model_selection import train_test_split
import xgboost as xgb
from  xgboost import XGBClassifier,XGBRegressor,XGBModel,DMatrix
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

# params, dtrain, num_boost_round=10, evals=(), obj=None, feval=None,
#           maximize=False, early_stopping_rounds=None, evals_result=None,
#           verbose_eval=True, xgb_model=None, callbacks=None, learning_rates=None

logger=logging.getLogger("xgb_syncer")
def xgb_train_fn(self,params,X_train,y_train,num_boost_round=700,lable="weiquan",early_stopping_rounds=20, verbose_eval=False, learning_rates=None,shuffle=False,bufferlist=None):
    dtrain=self.DMatrix(X_train,y_train)
    watchlist = [(dtrain, 'train')]
    print("begin work")
    if lable is None:
        print("not label ")
        model = self.train(params, dtrain, num_boost_round=num_boost_round, evals=watchlist,early_stopping_rounds=early_stopping_rounds,verbose_eval=verbose_eval,learning_rates=learning_rates)
    else :
        model=self.train(params,dtrain, num_boost_round=num_boost_round, evals=watchlist,early_stopping_rounds=early_stopping_rounds,verbose_eval=verbose_eval,learning_rates=learning_rates)
    # model_save_key=None
    # if mongo_cli !=None:
    #         print("will sync save model")
    #         model_save_key=save_modelfile_gridfs(self=model,mongo_cli=mongo_cli)
    #         print("mongodb key")
    #         print(model_save_key)
    #         model_config=ModelConfig(model_save_key, config=model, tag=model_save_key),
    #         fit_event = FitEvent(model, model_config, X_train, params)
    #         print("fit event create finish")
    # else:
    fit_event=FitEvent(model,self,X_train,params)
    if bufferlist != None:
        bufferlist.append(fit_event)
    else:
        Syncer.instance.add_to_buffer(event=fit_event)
    print("get model")
    self.params=params
    def get_params(self):
        return self.params

    setattr(xgb,'get_params',get_params)
    setattr(ModelConfig, 'get_params', get_params)
    return model

def XGBRegressor_fit_fn(self, X_train, y_train,max_depth, n_estimators,sample_weight=None,bufferlist=None):
    if type(self)==XGBRegressor or isinstance(self,XGBRegressor):
        model=self(n_estimators=n_estimators, max_depth=max_depth).fit(X_train, y_train)
    else :
        model = self.XGBRegressor(n_estimators=n_estimators, max_depth=max_depth).fit(X_train, y_train)
    fit_event = FitEvent(model, self, X_train)
    if bufferlist !=None:
        bufferlist.append(fit_event)
    else :
        Syncer.instance.add_to_buffer(fit_event)
    return model

def XGBClassifier_fit_fn(self, X_train, y_train,max_depth=3, n_estimators=100,objective='reg:linear',silent=0,nthread=-1,sample_weight=None,bufferlist=None):
   if type(self)==XGBClassifier or isinstance(self,XGBClassifier):
       model = self.XGBClassifier(nthread=nthread, max_depth=max_depth, silent=silent, objective=objective,n_estimators=n_estimators).fit(X_train,y_train)
   else:
        model=self.XGBClassifier(nthread=nthread, max_depth=max_depth, silent=silent,objective=objective, n_estimators=n_estimators).fit(X_train,y_train)
   fit_event = FitEvent(model, self, X_train)
   if bufferlist !=None:
       bufferlist.append(fit_event)
   else:
        Syncer.instance.add_to_buffer(fit_event)
   return model




def convert_prediction_to_event(model, predict_array, x,bufferlist=None):
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
    if bufferlist!=None:
        bufferlist.append(predict_event)
    else :
        Syncer.instance.add_to_buffer(predict_event)
    return predict_array


def xgb_predict_fn(self, df,bufferlist):
    """
    Overrides the predict function for models, provided that the predict
    function takes in one argument.
    """
    x=xgb.DMatrix(df)
    predict_array = self.predict(x)
    return convert_prediction_to_event(self, predict_array, df,bufferlist)
   # return predict_array


def xgb_predict_proba_fn(self, x):
    """
    Overrides the predict_proba function for models.
    """
    predict_array = self.predict_proba(x)
    return convert_prediction_to_event(self, predict_array, x)



def xgb_fit_cv_sync(self,train_x,train_y,num_booster,objective='reg:linear' ,eval_metric='mae',  nfold=3, early_stopping_rounds=20, verbose_eval=False,shuffle=False):
    random_seed = list(range(10000, 20000, 100))
    gamma = [i / 1000.0 for i in range(0, 300, 3)]
    max_depth = [3,4,5, 6, 7,8]
    lambd = list(range(400, 600, 2))
    subsample = [i / 1000.0 for i in range(500, 700, 2)]
    colsample_bytree = [i / 1000.0 for i in range(550, 750, 4)]
    min_child_weight = [i / 1000.0 for i in range(250, 550, 3)]

    np.random.shuffle(random_seed)
    np.random.shuffle(gamma)
    np.random.shuffle(max_depth)
    np.random.shuffle(lambd)
    np.random.shuffle(subsample)
    np.random.shuffle(colsample_bytree)
    np.random.shuffle(min_child_weight)
    # GridSearchCV()
    model_list=[]
    for i in range(5):
        model=xgb_fit_line_sync(train_x,train_y,num_booster,random_seed[i],gamma[i],max_depth[i%3],lambd[i],subsample[i],colsample_bytree[i],min_child_weight[i],objective,eval_metric)
        model_list.append(model)
    return  model_list



def xgb_fit_line_sync(self,train_x,train_y,num_booster,random_seed,gamma,max_depth,lambd,subsample,colsample_bytree,min_child_weight,objective='reg:linear' ,eval_metric='mae'):
    params={
            'booster':'gbtree',
            'objective': objective,
            'scale_pos_weight': float(len(train_y)-sum(train_y))/float(sum(train_y)),
            'eval_metric': eval_metric,
            'gamma':gamma,
            'max_depth':max_depth,
            'lambda':lambd,
            'subsample':subsample,
            'colsample_bytree':colsample_bytree,
            'min_child_weight':min_child_weight,
            'eta': 0.2,
            'seed':random_seed,
            'nthread':8
	 }
    dtrain=xgb.DMatrix(train_x,train_y,feature_names=[str(i) for i in list(train_x.columns)])
    watchlist  = [(dtrain,'train')]
    # history=xgb.cv(params, dtrain,num_boost_round= num_booster, nfold=nfold,early_stopping_rounds=early_stopping_rounds, verbose_eval=False, shuffle=False)
    # best_nrounds = int((history.shape[0] - early_stopping_rounds) / (1 - 1 / nfold))

    model = xgb.train(params,dtrain,num_booster,early_stopping_rounds=int(0.8*num_booster),evals=watchlist)
    fit_event=FitEvent(model,self,train_x,params)
    Syncer.instance.add_to_buffer(fit_event)
    return model

def cv_sync_fn(self, params,Dtrain,num_boost_round=100, nfold=3,early_stopping_rounds=20, verbose_eval=False, shuffle=False):
    results=xgb.cv(params, Dtrain,nfold=nfold, num_boost_round=num_boost_round, early_stopping_rounds=early_stopping_rounds, verbose_eval=verbose_eval, shuffle=shuffle)
    best_nrounds = int((results.shape[0] - early_stopping_rounds) / (1 - 1 / nfold))
    watchlist = [(Dtrain, 'train')]
    model = xgb.train(params,Dtrain,best_nrounds,evals=watchlist)
    fit_event=FitEvent(model,self,Dtrain,params)
    Syncer.instance.add_to_buffer(fit_event)
    return model

def xgb_transform_fn(self, x):
    """
    Overrides the transform function for models, provided that the
    transform function takes in one argument.
    """
    transformed_output = self.transform(x)
    if type(transformed_output) is np.ndarray:
        new_df = pd.DataFrame(transformed_output)
    else:
        new_df = pd.DataFrame(transformed_output.toarray())
    transform_event = TransformEvent(x, new_df, self)
    Syncer.instance.add_to_buffer(transform_event)
    return transformed_output


def xgb_fit_transform_fn(self, x, y=None, **fit_params):
    """
    Overrides the fit_transform function for models.
    Combines fit and transform functions.
    """
    df = x
    # Certain fit functions only accept one argument
    if y is None:
        fitted_model = self.fit(x, **fit_params)
    else:
        fitted_model = self.fit(x, y, **fit_params)
    fit_event = FitEvent(fitted_model, self, df)
    Syncer.instance.add_to_buffer(fit_event)
    transformed_output = fitted_model.transform(x)
    if type(transformed_output) is np.ndarray:
        new_df = pd.DataFrame(transformed_output)
    else:
        new_df = pd.DataFrame(transformed_output.toarray())
    transform_event = TransformEvent(x, new_df, fitted_model)
    Syncer.instance.add_to_buffer(transform_event)
    return transformed_output


def fit_fn_pipeline(self, x, y):
    """
    Overrides the Pipeline model's fit function
    """
    # Check if pipeline contains valid estimators and transformers
    check_valid_pipeline(self.steps)

    # Make Fit Event for overall pipeline
    pipeline_model = self.fit(x, y)
    pipeline_fit = FitEvent(pipeline_model, self, x)

    # Extract all the estimators from pipeline
    # All estimators call 'fit' and 'transform' except the last estimator
    # (which only calls 'fit')
    names, sk_estimators = zip(*self.steps)
    estimators = sk_estimators[:-1]
    last_estimator = sk_estimators[-1]

    transform_stages = []
    fit_stages = []
    cur_dataset = x

    for index, estimator in enumerate(estimators):
        old_df = cur_dataset
        model = estimator.fit(old_df, y)
        transformed_output = model.transform(old_df)

        # Convert transformed output into a proper pandas DataFrame object
        if type(transformed_output) is np.ndarray:
            new_df = pd.DataFrame(transformed_output)
        else:
            new_df = pd.DataFrame(transformed_output.toarray())

        cur_dataset = transformed_output

        # populate the stages
        transform_event = TransformEvent(old_df, new_df, model)
        transform_stages.append((index, transform_event))
        fit_event = FitEvent(model, estimator, old_df)
        fit_stages.append((index, fit_event))

    # Handle last estimator, which has a fit method (and may not have
    # transform)
    old_df = cur_dataset
    model = last_estimator.fit(old_df, y)
    fit_event = FitEvent(model, last_estimator, old_df)
    fit_stages.append((index + 1, fit_event))

    # Create the pipeline event with all components
    pipeline_event = PipelineEvent(pipeline_fit, transform_stages, fit_stages)

    Syncer.instance.add_to_buffer(pipeline_event)

def compute_roc_auc_sync(self,test_y,y_pred,df,prediction_col='',label_col='',bufferlist=None,**params):
    roc_auc=metrics.roc_auc_score(test_y,y_pred)
    print("compute is "+ str(roc_auc))
    metrics_event=MetricEvent(df,self,label_col,prediction_col,metrics.roc_auc_score.__name__,roc_auc)
    if bufferlist != None:
        bufferlist.append(metrics_event)
    else:
        Syncer.instance.add_to_buffer(metrics_event)

    return roc_auc

def compute_mean_absolute_error(self,test_y,y_pred,df,prediction_col='',label_col='',bufferlist=None,**params):
    mae=mean_absolute_error(test_y,y_pred=y_pred)
    print("compute is "+ str(mae))
    metrics_event=MetricEvent(df,self,label_col,prediction_col,mean_absolute_error.__name__,mae)
    if bufferlist != None:
        bufferlist.append(metrics_event)
    else:
        Syncer.instance.add_to_buffer(metrics_event)
    return mae

def  compute_mean_squared_error(self,test_y,y_pred,df,prediction_col='',label_col='',bufferlist=None,**params):
    mse=mean_squared_error(test_y,y_pred=y_pred)
    metrics_event=MetricEvent(df,self,label_col,prediction_col,mean_squared_error.__name__,mse)
    if bufferlist != None:
        bufferlist.append(metrics_event)
    else:
        Syncer.instance.add_to_buffer(metrics_event)
    return mse


def compute_accuracy_score_sync(self,test_y,y_pred,df,prediction_col='',label_col='',bufferlist=None,**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    accuracy_score=metrics.accuracy_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,self,label_col,prediction_col,metrics.accuracy_score.__name__,accuracy_score)
    if bufferlist != None:
        bufferlist.append(metrics_event)
    else:
        Syncer.instance.add_to_buffer(metrics_event)
    return accuracy_score

def compute_recall_score_sync(self,test_y,y_pred,df,prediction_col='',lable_col='',bufferlist=None,**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    recall_score=metrics.recall_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,self,lable_col,prediction_col,metrics.recall_score.__name__,recall_score)
    if bufferlist != None:
        bufferlist.append(metrics_event)
    else:
        Syncer.instance.add_to_buffer(metrics_event)
    return recall_score

def compute_precision_score_sync(self,test_y,y_pred,df,prediction_col='',lable_col='',bufferlist=None,**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    print("hello precision")
    precision_score=metrics.precision_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,self,lable_col,prediction_col,metrics.precision_score.__name__,precision_score)
    if bufferlist != None:
        bufferlist.append(metrics_event)
    else:
        Syncer.instance.add_to_buffer(metrics_event)
    print(Syncer.buffer_list)
    return precision_score

def compute_f1_score_sync(self,test_y,y_pred,df,prediction_col='',lable_col='',bufferlist=None,**params):
    y_pred_binary = (y_pred >= 0.5) * 1
    f1_score=metrics.f1_score(test_y,y_pred_binary)
    metrics_event=MetricEvent(df,self,lable_col,prediction_col,metrics.f1_score.__name__,f1_score)
    if bufferlist != None:
        bufferlist.append(metrics_event)
    else:
        Syncer.instance.add_to_buffer(metrics_event)
    return  f1_score


def check_valid_pipeline(steps):
    """
    Helper function to check whether a pipeline is constructed properly. Taken
    from original sklearn pipeline source code with minor modifications,
    which are commented below.
    """
    names, estimators = zip(*steps)
    transforms = estimators[:-1]
    estimator = estimators[-1]

    for t in transforms:
        # Change from original scikit: checking for "fit" and "transform"
        # methods, rather than "fit_transform" as each event is logged
        # separately to database
        if not (hasattr(t, "fit")) and hasattr(t, "transform"):
            raise TypeError("All intermediate steps of the chain should "
                            "be transforms and implement fit and transform"
                            " '%s' (type %s) doesn't)" % (t, type(t)))

    if not hasattr(estimator, "fit"):
        raise TypeError("Last step of chain should implement fit "
                        "'%s' (type %s) doesn't)"
                        % (estimator, type(estimator)))


def fit_fn_grid_search_fn(self, x_train, y_train,params,cv=5,scoring='mae',n_jobs=2,verbose=2,bufferlist=None):
    """
    Overrides GridSearch Cross Validation's fit function
    """
    gridscv=GridSearchCV(self,params,cv=cv,scoring=scoring,n_jobs=n_jobs,verbose=verbose)
    gridscv.fit(x_train,y_train)

    # [input_data_frame, cross_validations, seed, evaluator, best_model,
    #     best_estimator, num_folds] = self.grid_cv_event

    # Calls SyncGridCVEvent and adds to buffer.
    grid_event = GridSearchCVEvent(x_train,gridscv,
                                   gridscv.best_params_, gridscv.best_estimator_,gridscv.best_estimator_, cv)
    Syncer.instance.add_to_buffer(grid_event)


def store_df_path(filepath_or_buffer, **kwargs):
    """
    Stores the filepath for a dataframe
    """
    df = pd.read_csv(filepath_or_buffer, **kwargs)
    Syncer.instance.store_path_for_df(df, str(filepath_or_buffer))
    return df


def train_test_split_fn(*arrays, **options):
    """
    Stores the split dataframes.
    """
    split_dfs = train_test_split(*arrays, **options)

    # Extract the option values to create RandomSplitEvent
    test_size = options.pop('test_size', None)
    train_size = options.pop('train_size', None)
    random_state = options.pop('random_state', None)
    if test_size is None and train_size is None:
        test_size = 0.25
        train_size = 0.75
    elif test_size is None:
        test_size = 1.0 - train_size
    else:
        train_size = 1.0 - test_size
    if random_state is None:
        random_state = 1
    main_df = arrays[0]
    weights = [train_size, test_size]
    result = split_dfs[:int(len(split_dfs) / 2)]
    random_split_event = RandomSplitEvent(
        main_df, weights, random_state, result)
    Syncer.instance.add_to_buffer(random_split_event)
    return split_dfs

def save_modelfile_gridfs(self,mongo_cli,collect='modeldb_metadata'):
#    log.info(msg="save model file to mongodb")
    #mongo_cli = MongoClient("localhost",27017)
    data_base =mongo_cli.get_database(collect)
    fs = gridfs.GridFS(data_base)
    import pickle
    print(vars(self))
    model_pkl_file= pickle.dumps(self)
    model_meta_primarykey=fs.put(model_pkl_file)
    print(model_meta_primarykey)
    return  model_meta_primarykey

        # with open(model.model_path(), 'rb') as fk:
        #     model_obj = pickle.load(fk)

    # read model primary key id  in mongodb gridfs load for model object
def query_model_by_gridfsid_model(mongo_cli,modelfile_id,collect='modeldb_metadata'):
    # log.info(msg="use id  query  model in modeldb")
    # if self.mongo_cli ==None:
    #      self.mongo_cli = MongoClient(self.host, self.mongodb_port)
    o_id=ObjectId(modelfile_id) ##!!!
    data_base = mongo_cli.get_database(collect)
    fs = gridfs.GridFS(data_base)
    model_file_inx = fs.get(o_id)
    model=pickle.loads(model_file_inx.read())
    return model

    #read model primary key id in mongodb gridfs and save on the disk path
def query_model_bygridfsid_save_disk(self,model_id,save_path, collect='modeldb_metadata'):
    log.info(msg="use id  query  model in gridfs and save to disk ")
    if self.mongo_cli == None:
        self.mongo_cli = MongoClient(self.host,self.mongodb_port)
    o_id = ObjectId(model_id)  ##!!!
    data_base = self.mongo_cli.get_database(collect)
    fs = gridfs.GridFS(data_base)
    model_file_inx = fs.get(o_id)
    with open(save_path, 'wb')as f:
        f.write(model_file_inx.read())

def add_model_savepath_to_fitEvent(self,model_obj,collect='modeldb_metadata'):
    gridfs_model_id=save_modelfile_gridfs(self,model_obj,collect)
    eventlist=Syncer.buffer_list
    for event in eventlist:
        if isinstance(event,FitEvent):
            eve=FitEvent(event)
            eve.model.fiepath=gridfs_model_id


def drop_columns(self, labels, **kwargs):
    """
    Overrides the "drop" function of pandas dataframes
    so event can be logged as a TransformEvent.
    """
    dropped_df = self.drop(labels, **kwargs)
    drop_event = TransformEvent(self, dropped_df, 'DropColumns')
    Syncer.instance.add_to_buffer(drop_event)
    return dropped_df


'''
End functions that extract information from scikit-learn, pandas and numpy
'''


class Syncer(with_metaclass(Singleton, ModelDbSyncerBase.Syncer)):

    # The Syncer class needs to have its own pointer to the singleton instance
    # for overidden sklearn methods to reference
    instance = None
    """
    This is the Syncer class for sklearn, responsible for
    storing events in the ModelDB.
    """
    # @classmethod
    # def init_sync_enable(cls):
    #
    #     local_id_to_path = {}
    #     cls.enable_xgboost_sync_functions(cls)
    #     # self.enable_pandas_sync_functions()
    #     Syncer = cls
    #     return Syncer
    def __init__(
            self, project_config, experiment_config, experiment_run_config,
            thrift_config=None):
        self.local_id_to_path = {}
        self.enable_xgboost_sync_functions()
        self.enable_pandas_sync_functions()

        Syncer.instance = self

        super(Syncer, self).__init__(project_config, experiment_config,
                                     experiment_run_config, thrift_config)

    def __str__(self):
        return "SklearnSyncer"

    '''
    Functions that turn classes specific to this syncer into equivalent
    thrift classes
    '''

    def set_buffer_list(self,buffer_list=None):
        if buffer_list !=None:
            for buffer in buffer_list:
                self.add_to_buffer(buffer)



    def set_columns(self, df):
        """
        Helper function to extract column names from a dataframe.
        Pandas dataframe objects are treated differently from
        numpy arrays.
        """
        if type(df) is pd.DataFrame:
            columns = df.columns.values
            if type(columns) is np.ndarray:
                columns = np.array(columns).tolist()
            for i in range(0, len(columns)):
                columns[i] = str(columns[i])
        else:
            columns = []
        return columns

    def setDataFrameSchema(self, df):
        """
        Helper function designated to extract the column schema
        within a dataframe.
        """
        data_frame_cols = []
        columns = self.set_columns(df)
        for i in range(0, len(columns)):
            columnName = str(columns[i])
            dfc = modeldb_types.DataFrameColumn(columnName, str(df.dtypes[i]))
            data_frame_cols.append(dfc)
        return data_frame_cols

    def convert_model_to_thrift(self, model):
        """
        Converts a model into a Thrift object with appropriate fields.
        """
        tid = self.get_modeldb_id_for_object(model)
        tag = self.get_tag_for_object(model)
        transformer_type = model.__class__.__name__
        t = modeldb_types.Transformer(tid, transformer_type, tag)
        return t

    def get_path_for_df(self, df):
        local_id = self.get_local_id(df)
        if local_id in self.local_id_to_path:
            return self.local_id_to_path[local_id]
        else:
            return ""

    def store_path_for_df(self, df, path):
        local_id = self.get_local_id(df)
        self.local_id_to_path[local_id] = path
        if local_id not in self.local_id_to_object:
            self.local_id_to_object[local_id] = df

    def convert_df_to_thrift(self, df):
        """
        Converts a dataframe into a Thrift object with appropriate fields.
        """
        tid = self.get_modeldb_id_for_object(df)
        tag = self.get_tag_for_object(df)
        filepath = self.get_path_for_df(df)

        dataframe_columns = self.setDataFrameSchema(df)
        modeldb_df = modeldb_types.DataFrame(
            tid, dataframe_columns, df.shape[0], tag, filepath)
        return modeldb_df

    def convert_spec_to_thrift(self, spec):
        """
        Converts a TransformerSpec object into a Thrift object with appropriate
        fields.
        """
        tid = self.get_modeldb_id_for_object(spec)
        tag = self.get_tag_for_object(spec)
        hyperparams = []
        if isinstance(spec,xgb.Booster):
             params = spec.get_params(spec)
        else:
            params=xgb.get_params(xgb)
        for param in params:
            hp = modeldb_types.HyperParameter(
                param,
                str(params[param]),
                type(params[param]).__name__,
                sys.float_info.min,
                sys.float_info.max)
            hyperparams.append(hp)
        ts = modeldb_types.TransformerSpec(tid, spec.__class__.__name__,
                                           hyperparams, tag)
        return ts

    def sync_all(self, metadata_path):
        super(Syncer,self).sync_all(metadata_path)

    def sync(self,buffer_list=None,save_key=None,sql_cli=None):
        super(Syncer, self).sync()
        if buffer_list!=None:
            self.set_buffer_list(buffer_list)
        else :
            if hasattr(self, 'experiment_run'):
                if isinstance(self.experiment_run, ExperimentRun):
                    experiment_runId=self.experiment_run.id
                    print(experiment_runId)
                    print(save_key)
                    #import  pymysql
                    #sql_cli=pymysql.connect(host=host,user=user,passwd=pwd,db=db,port=port,charset='utf8')
                    # cursor=sql_cli.cursor()
                    if save_key!=None and sql_cli!=None: #"5bee664d87c5f627186b020b"
                        cursor = sql_cli.cursor()
                        sql="update ExperimentRun set `sha` = '"+str(save_key )+" ' where `id`= " + str(experiment_runId)
                        print(sql)
                        cursor.execute(sql)
                        sql_cli.commit()


    # def sync(self,model_obj=None,monogo_cli=None,collect='modeldb_metadata'):
    #     model_save_key=None
    #     if model_obj!=None and MongoClient !=None:
    #         print("will sync save model")
    #         model_save_key=save_modelfile_gridfs(self=model_obj,mongo_cli=monogo_cli)
    #     super(Syncer, self).sync()
    #
        #if hasattr(self, 'experiment_run'):
            #self.experiment_run.sha=model_save_key
 #           ner=NewExperimentRun(description=str(model_save_key), sha=str(model_save_key))
           #  nepro=Project(-1,"gameng")
           #
           #  print(vars(self.experiment_run))
#            self.set_experiment_run(ner)
#             print(type(self.experiment_run))
#             print(self.experiment.id)
#             if isinstance(self.experiment_run,ExperimentRun):

   #              # self.project=nepro
   #              # print(self.project.id)
   #              # self.experiment=Experiment(-1,self.project.id,name='defaultzz')
   #              print(self.experiment.id)
              #  self.experiment_run=ExperimentRun(id=87,experimentId=1,description='hah',sha=model_save_key)
   #
   #              print(vars(self.experiment_run))
            # print(self.experiment_run.sha)
            # self.set_experiment_run(ner)
            # import  time
            # time.sleep(12)
               # self.__delattr__('experiment_run')
                #super(Syncer,self).sync()
    # def set_experiment_run(self, experiment_run_config,experimentid):
    #     self.experiment_run = experiment_run_config.to_thrift()
    #     self.experiment_run.experimentId = experimentid
    #     experiment_run_event = ExperimentRunEvent(self.experiment_run)
    #     self.buffer_list.append(experiment_run_event)
    #     self.sync()
    '''
    End Functions that turn classes specific to this syncer into equivalent
    thrift classes
    '''

    '''
    Enable sync functionality on various functions
    '''

    def enable_pandas_sync_functions(self):
        """
        Adds the read_csv_sync function, allowing users to automatically
        track dataframe location, and the drop_sync function, allowing users
        to track dropped columns from a dataframe.
        """
        setattr(pd, "read_csv_sync", store_df_path)
        setattr(pd.DataFrame, "drop_sync", drop_columns)

    def enable_xgboost_sync_functions(self):
        """
        This function extends the scikit classes to implement custom
        *Sync versions of methods. (i.e. fit_sync() for fit())
        Users can easily add more models to this function.
        """
        # Linear Models (transform has been deprecated)
        setattr(xgb,'train_sync',xgb_train_fn)
        setattr(xgb, 'load_model_sync', query_model_by_gridfsid_model)

        setattr(xgb.Booster,'auc_sync',compute_roc_auc_sync)
        setattr(xgb.Booster,'mae_sync' ,compute_mean_absolute_error)
        setattr(xgb.Booster,'mse_sync',compute_mean_squared_error)
        # setattr(xgb,'get_params',get_params)
        setattr(xgb.XGBClassifier,'fit_sync',XGBClassifier_fit_fn)
        setattr(xgb.XGBRegressor,'fit_sync',XGBRegressor_fit_fn)

        for  cls_name in [xgb.XGBRegressor,xgb.XGBClassifier,xgb.Booster,xgb.XGBModel]:
            setattr(cls_name,'predict_sync',xgb_predict_fn)
            setattr(cls_name, 'auc_sync', compute_roc_auc_sync)
            setattr(cls_name, 'mae_sync', compute_mean_absolute_error)
            setattr(cls_name, 'mse_sync', compute_mean_squared_error)
            setattr(cls_name,'precision_sync',compute_precision_score_sync)
            setattr(cls_name, 'recall_sync', compute_recall_score_sync)
            setattr(cls_name, 'accuracy_sync', compute_accuracy_score_sync)
            setattr(cls_name, 'f1_score_sync', compute_f1_score_sync)
            setattr(cls_name,'save_model_sync', save_modelfile_gridfs)


        for cls_name in [LogisticRegression, LinearRegression,
                           CalibratedClassifierCV, RandomForestClassifier,
                           BaggingClassifier,RandomForestRegressor]:
            setattr(cls_name, 'auc_sync', compute_roc_auc_sync)
            setattr(cls_name, 'mae_sync', compute_mean_absolute_error)
            setattr(cls_name, 'mse_sync', compute_mean_squared_error)
            setattr(cls_name,'precision_sync',compute_precision_score_sync)
            setattr(cls_name, 'recall_sync', compute_recall_score_sync)
            setattr(cls_name, 'accuracy_sync', compute_accuracy_score_sync)
            setattr(cls_name, 'f1_score_sync', compute_f1_score_sync)


        for cls_name in [xgb.XGBRegressor,xgb.XGBClassifier]:
            setattr(cls_name,'predict_proba_sync',xgb_predict_proba_fn)

        setattr(xgb,'cv_sync',cv_sync_fn)
        # Pipeline model
        for class_name in [Pipeline]:
            setattr(class_name, "fit_sync", fit_fn_pipeline)

        # # Grid-Search Cross Validation model
        # for class_name in [GridSearchCV]:
        #     setattr(class_name, "fit_sync", fit_fn_grid_search)
        #     setattr(class_name, "predict_sync", predict_fn)
        #
        # # Train-test split for cross_validation
        # setattr(cross_validation, "train_test_split_sync", train_test_split_fn)
        # setattr(cross_validation, "cross_val_score_sync", cross_val_score_fn)
