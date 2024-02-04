import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')
from src.components.data_transformation import DataTransformation
from src.components.model_trainner import ModelTrainer
from src.components.data_ingestion import DataIngestion



if __name__=='__main__':
    try:
        logging.info("training pipeline has initiated")
        data=DataIngestion()
        train_path,test_path=data.initiate_data_ingestion()
        model=ModelTrainer()
        data_trans=DataTransformation()
        train,test,file=data_trans.initaite_data_transformation(train_path=train_path,test_path=test_path)
        model.initate_model_training(train_array=train,test_array=test)
        logging.info("Training pipeline has done successfully ")
    except Exception as e:
        raise CustomException(e,sys)