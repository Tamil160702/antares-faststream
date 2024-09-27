from fastapi import HTTPException
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

from config.config import Config
from common.logger import Logger


class ScyllaHelper():
  def __init__(self):
      self.config = Config()
      self.log = Logger()  
      self.scylla = None

  def getScyllaCluster(self):
    try:
      #TODO: Add authentication to the scylla keyspace and include the logic here
      if self.scylla is None:
        self.scylla = Cluster([self.config.Scylla.host], port=self.config.Scylla.port)
      return self.scylla
    except Exception as err:
      raise HTTPException(status_code=500, detail="Error Connecting to DB Service")
    
  async def readFromScylla(self, query, *args):
    try:
      scylla = self.getScyllaCluster()
      session = scylla.connect()
      session.set_keyspace(self.config.Scylla.keyspace)
      session.row_factory = dict_factory

      result = session.execute(query, *args)
      
      self.log.debug("readFromScylla:::Result from ScyllaDB: {0}", result)
      
      return result

    except Exception as err:
      self.log.error("Error in Executing Scylla Query: {0} - {1} - {2}", str(err), query, args)
      raise HTTPException(status_code=500, detail="Internal Server Error")

  async def executeInScylla(self, query, *args):
    try:
      scylla = self.getScyllaCluster()
      session = scylla.connect()
      session.set_keyspace(self.config.Scylla.keyspace)
      result= session.execute(query, *args)
      self.log.debug("readFromScylla:::Result from ScyllaDB: {0}", result)
      return result  

    except Exception as err:
      self.log.error("Error in Executing Scylla Query: {0}", err)
      self.log.error("Error in Executing Scylla Query: {0} - {1} - {2}", str(err), query, args)
      raise HTTPException(status_code=500, detail="Internal Server Error")
  
  async def createInScylla(self, query):
    try:
      scylla = self.getScyllaCluster()
      session = scylla.connect()
      session.set_keyspace(self.config.Scylla.keyspace)

      result = session.execute(query)
      self.log.debug("CreateFromScylla:::Result from ScyllaDB: {0}", result)
      
      return result  

    except Exception as err:
      print(err)
      self.log.error("Error in Executing Scylla Query: {0}", err)
      raise HTTPException(status_code=500, detail="Internal Server Error")
    
  async def execScyllastatement(self, query):
    try:
      scylla = self.getScyllaCluster()
      session = scylla.connect()
      session.set_keyspace(self.config.Scylla.keyspace)
      session.row_factory = dict_factory

      result = session.execute(query)

      self.log.debug("readFromScylla:::Result from ScyllaDB: {0}", result)
      
      return result

    except Exception as err:
      self.log.error("Error in Executing Scylla Query: {0} - {1} ", str(err), query)
      raise HTTPException(status_code=500, detail="Internal Server Error")

  async def get_table_schema(self, table_name):
    try:
      scylla = self.getScyllaCluster()
      session = scylla.connect()
      session.set_keyspace(self.config.Scylla.keyspace)
      metadata = scylla.metadata.keyspaces[self.config.Scylla.keyspace].tables[table_name]
      columns = metadata.columns
      column_data_types = {}
      for column_name, column_metadata in columns.items():
          column_data_types[column_name] = str(column_metadata)
      columns_type = {}
      for data_type_key,data_type_value in column_data_types.items():
        data_type_value = data_type_value.split(data_type_key+' ',1)
        columns_type[data_type_key]=data_type_value[1]
      self.log.debug('result columns_type::{}',columns_type)

      return columns_type

    except Exception as err:
      self.log.error("Error in fetching schema for table: {1} - {0} ", str(err), table_name)
      raise HTTPException(status_code=500, detail="Internal Server Error")

  async def get_type_schema(self, type_name):
    try:
      scylla = self.getScyllaCluster()
      session = scylla.connect()
      session.set_keyspace(self.config.Scylla.keyspace)
      metadata = scylla.metadata.keyspaces[self.config.Scylla.keyspace].user_types[type_name]
      type_field_values ={}
      # field_name=metadata.field_names
      n=0
      for i in metadata.field_names:
        type_field_values[i] = metadata.field_types[n]
        n=n+1
      return type_field_values

    except Exception as err:
      self.log.error("Error in fetching schema for type: {1} - {0} ", str(err), type_name)
      raise HTTPException(status_code=500, detail="Internal Server Error")
    