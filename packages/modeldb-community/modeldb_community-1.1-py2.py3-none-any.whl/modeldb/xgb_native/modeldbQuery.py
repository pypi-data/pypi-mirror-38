
from modeldb.thrift.modeldb.ModelDBService import Client

from modeldb.xgb_native.XGBModelDBSyncer import *
import  gridfs
from bson.objectid import ObjectId

import  logging
log=logging.getLogger(__name__)
class ModeldbQuery:

    def __init__(self,syncer_obj:Syncer,mongo_cli=None):
        print("init client")
        self.syncer_obj =syncer_obj
        if mongo_cli !=None:
            self.mongo_cli=mongo_cli
        cli = self.syncer_obj.client
        cliz = Client(cli._iprot)
        cliz.testConnection()
        self.client=cliz

    # def __init__(self,host='localhost',port=6543,mongo_host='local_host',mongo_port=27017,name='model_con',author='muller',desc='test_con',exrun='data_brain'):
    #     self.thrift_host=host
    #     self.thrift_port=port
    #     #self.project_id=project_id
    #     self.mongo_cli=MongoClient(mongo_host,mongo_port)
    #     self.syncer_obj = Syncer(
    #         NewOrExistingProject(name, author, desc),
    #         DefaultExperiment(),
    #         NewExperimentRun(exrun), ThriftConfig(host=host))
    #
    #     cli = self.syncer_obj.client
    #     cliz = Client(cli._iprot)
    #     cliz.testConnection()
    #     self.client=cliz

    def get_thrift_client(self):
        cli=Client(self.thrift_host)
        cliz = Client(cli._iprot)
        cliz.testConnection()

        return cliz


    def query_project(self):
        return self.syncer_obj.project


    def query_all_projectlist(self):
        project_list=[]
        pros=self.client.getProjectOverviews()
        for pro in pros:
            project_list.append(pro.project)
        return  project_list

    def query_projectlist_byTrainerName(self,trainer):
        project_list=[]
        pros=self.client.getProjectOverviews()
        for pro in pros:
            if str(pro.author)==trainer:
                project_list.append(pro)
        return project_list

    def query_projectlist_byProjectname(self,proname):
        project_list=[]
        pros=self.client.getProjectOverviews()
        for pro in pros:
            if str(pro.name) ==proname:
                project_list.append(pro)
        return project_list

    def query_projectlist_bydesc(self, desc):
        project_list=[]
        pros=self.client.getProjectOverviews()
        for pro in pros:
            if desc in str(pro.description):
                project_list.append(pro)
        return project_list

    def query_modelList_byProjectId(self,projectId):
        modelList=[]
        runs_exps =self.client.getRunsAndExperimentsInProject(projectId)
        for exRun in runs_exps.experimentRuns:
            model_res = self.client.getExperimentRunDetails(exRun.id).modelResponses
            if isinstance(model_res,list):
                model_res=list(model_res)
                if len(model_res):
                    print(model_res[0])
                    modelList.append(model_res[0])
        return modelList

    def query_model_byExperimentRunId(self,experimentrunId):
        model_res = self.client.getExperimentRunDetails(experimentrunId).modelResponses
        if len(list(model_res)):
            print(model_res)
            return  model_res[0]
        else:
            print("no model exist !!!")
            return  None

    def query_modellist_syncer(self):
        project=self.syncer_obj.project
        projectId=project.id
        modelList=[]
        runs_exps =self.client.getRunsAndExperimentsInProject(projectId)

        for exRun in runs_exps.experimentRuns:
            model_res = self.client.getExperimentRunDetails(exRun.id).modelResponses
            if len(list(model_res)):
                print(model_res[0])
                modelList.append(model_res[0])
        return modelList

    # def query_models_syncer(self):
    #     project=self.syncer_obj.project
    #     projectId=project.id
    #     modelList = []
    #     keyValueMap={}
    #     modelId_list= self.client.getModelIds(keyValueMap)
    #     for modelId in modelId_list:
    #         model=self.client.getModel(modelId)
    #         modelList.append(model)
    #     return modelList


    def query_model_byClient(self,modelId):
        model= self.client.getModel(modelId)
        if model !=None:
            print("print model struct")
            print(vars(model))
            return  model
        else:
            return None

    def query_model_hyperList(self,modelId):
        model=self.client.getModel(modelId)
        if model !=None:
            print("type model ")
            print(model.metadata)
            return model.metadata
        #     if model.metadata !=None:
        #         print(vars(model.metadata))
        #         return  model.metadata
        #     else:
        #         print(vars(model.hyperparameters))
        #         return model.hyperparameters
        # else:
        #     return None


    def query_model_creatime(self,modelId):
        model = self.client.getModel(modelId)
        if model !=None:
            return model.filepath
    def query_gridfsId_bymodelId(self,modelId):
        model = self.client.getModel(modelId)
        if model !=None:
            print(model.sha)
            return model.sha

    def query_gridfsId_byExperimentRunId(self,experimentrunId):
        model_res = self.client.getExperimentRunDetails(experimentrunId).modelResponses
        if len(list(model_res)):
            #print(model_res)
            model = self.client.getModel(model_res[0].id)
            if model !=None:
                print("ouput sha grid fs ")
                print(model.sha)
                return model.sha

    def query_model_metrics(self,modelId):
        model = self.client.getModel(modelId)
        if model !=None:
            return model.metrics

    def query_model_df(self,modelId):
        model = self.client.getModel(modelId)
        if model !=None:
            return model.trainingDataFrame

    # def load_model_from_gridfs_byOId(self,oId, mongo_db='modeldb_metadata'):
    #     data_base =self.mongo_cli.get_database(mongo_db)
    #     # for  k in data_base.list_collections():
    #     #     print(k)
    #     fs = gridfs.GridFS(data_base)
    #     print(fs)
    #     file = fs.get(ObjectId(oId))
    #     return  file
    # def load_model_from_gridfs_byModelId(self,modelId,mongo_db='modeldb_metadata'):
    #     model = self.client.getModel(modelId)
    #     oId=model.filepath
    #     data_base =self.mongo_cli.get_database(mongo_db)
    #     # for  k in data_base.list_collections():
    #     #     print(k)
    #     fs = gridfs.GridFS(data_base)
    #     print(fs)
    #     file = fs.get(ObjectId(oId))
    #     return  file

    def del_project(self,projectid):
        return None

    def del_model(self,modelid):
        return  None

    def save_modelfile_gridfs(self, model_obj,mongo_cli=None, collect='modeldb_metadata'):
        log.info(msg="save model file to mongodb")
        if self.mongo_cli == None:
            self.mongo_cli = mongo_cli #MongoClient(self.host, self.mongodb_port)
        data_base = self.mongo_cli.get_database(collect)
        fs = gridfs.GridFS(data_base)
        import pickle
        model_pkl_file = pickle.dumps(model_obj)
        model_meta_primarykey = fs.put(model_pkl_file)
        print(model_meta_primarykey)
        return model_meta_primarykey
        # with open(model.model_path(), 'rb') as fk:
        #     model_obj = pickle.load(fk)

        # read model primary key id  in mongodb gridfs load for model object

    def load_model_by_gridfsid_model(self, modelfile_id, mongo_cli=None,collect='modeldb_metadata'):
        log.info(msg="use id  query  model in modeldb")
        if self.mongo_cli == None:
            self.mongo_cli = mongo_cli #MongoClient(self.host, self.mongodb_port)
        o_id = ObjectId(modelfile_id)  ##!!!
        data_base = self.mongo_cli.get_database(collect)
        fs = gridfs.GridFS(data_base)
        model_file_inx = fs.get(o_id)
        model = pickle.loads(model_file_inx.read())
        return model

        # read model primary key id in mongodb gridfs and save on the disk path

    def load_model_bygridfsid_save_disk(self, model_id, save_path,mongo_cli=None, collect='modeldb_metadata'):
        log.info(msg="use id  query  model in gridfs and save to disk ")
        if self.mongo_cli == None:
            self.mongo_cli =mongo_cli # MongoClient(self.host, self.mongodb_port)
        o_id = ObjectId(model_id)  ##!!!
        data_base = self.mongo_cli.get_database(collect)
        fs = gridfs.GridFS(data_base)
        model_file_inx = fs.get(o_id)
        with open(save_path, 'wb')as f:
            f.write(model_file_inx.read())

    # def get_buffer_list(self,modelid):

    # def query_model