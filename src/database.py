import cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from src.exception import CustomException
from src.logger import logging
import os
import sys
from datetime import datetime
import uuid

class DatabaseConfig:
  
  def __init__(self):
    pass
  
  
  def Configaration_keyspace(self):
    try:
        cloud_config= {
        'secure_connect_bundle': 'secure-connect-store-sales-db.zip'
        }
        auth_provider = PlainTextAuthProvider('CxMgoKmEDZGbtjaoMHxfjJED', 'xtX6hs2xM0geGgwyag,M9_8dl3IsQ5XY7jiuCBi.MAsyUAxe14d7x9jbeb5ZLb6ot+XKgryFOLKlAMLZPGnuEzvnaA6eFXEGieFEMlrc6TlzC50-8SX,PYKBiPjQSFOt')
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect()

        row = session.execute("select release_version from system.local").one()
        print(row)
        logging.info(f"{row[0]}.Successfully connect with key-space")
        return session
    except Exception as e:
       raise CustomException(e,sys)
    
  def create_table(self,session):
    try:
        quary='use store_keyspace'
        session.execute(quary)
        print('inside the keyspace')
        #create a table 
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS BigMart_sales1(
                id uuid PRIMARY KEY,
                Item_Identifier varchar,
                item_weight float,
                Item_Fat_Content varchar,
                Item_Visibility float,
                Item_Type varchar,
                Item_MRP float,
                Outlet_Age float,
                Outlet_Size varchar,
                Outlet_Location_Type varchar,
                Outlet_Type varchar,
                Item_Outlet_Sales float,
                insertion_time timestamp
                
            )
        """
        session.execute(create_table_query)
        print(f'successfully create table ')
        
    except Exception as e:
     print('error occured',e)
     raise CustomException(e,sys)
    

  def put_values(self,session,Item_Identifier,item_weight,Item_Fat_Content,Item_Visibility,Item_Type,Item_MRP,
                 Outlet_Age,Outlet_Size,Outlet_Location_Type,Outlet_Type,Item_Outlet_Sales):
    
    try:
     quary='use store_keyspace'
     session.execute(quary)
     print('inside the keyspace')
     
     new_uuid = uuid.uuid4()
     current_time = datetime.now()

     insert_query = f"""
        INSERT INTO BigMart_sales1(id,Item_Identifier, item_weight,Item_Fat_Content,
        Item_Visibility,Item_Type, Item_MRP,Outlet_Age,Outlet_Size,Outlet_Location_Type,
        Outlet_Type,Item_Outlet_Sales,insertion_time) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
     """

     session.execute(insert_query,
                     (new_uuid,Item_Identifier,item_weight,Item_Fat_Content,
                      Item_Visibility,Item_Type,Item_MRP,Outlet_Age,Outlet_Size,
                      Outlet_Location_Type,Outlet_Type,Item_Outlet_Sales,current_time))
     logging.info('successfully insert data into Cassandra database')
    except Exception as e:
     print('error occured',e)
     raise CustomException(e,sys)
     




       