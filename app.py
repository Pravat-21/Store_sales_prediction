from flask import Flask,request,render_template,redirect
import numpy as np
import pandas as pd
from src.pipeline.prediction_pipeline import CustomData,PredictPipeline
from src.database import DatabaseConfig
from src.logger import logging

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    else:
        data=CustomData(
            Item_Identifier=request.form.get('Item_Identifier'),
            Item_Weight=float(request.form.get('Item_Weight')),
            Item_Fat_Content=request.form.get('Item_Fat_Content'),
            Item_Visibility=float(request.form.get('Item_Visibility')),
            Item_Type=request.form.get('Item_Type'),
            Item_MRP=float(request.form.get('Item_MRP')),
            Outlet_Age=float(request.form.get('Outlet_Age')),
            Outlet_Size=request.form.get('Outlet_Size'),
            Outlet_Location_Type=request.form.get('Outlet_Location_Type'),
            Outlet_Type=request.form.get('Outlet_Type')

        )
        pred_df=data.get_data_as_data_frame()
        logging.info(pred_df)
        #print(pred_df)
        #print("Before Prediction")
        table_html = pred_df.to_html(index=False)

        predict_pipeline=PredictPipeline()
        #print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        #print("after Prediction")
        #insert all the data into my Cassandra Database:
        Item_Identifier=str(request.form.get('Item_Identifier'))
        Item_Weight=float(request.form.get('Item_Weight'))
        Item_Fat_Content=str(request.form.get('Item_Fat_Content'))
        Item_Visibility=float(request.form.get('Item_Visibility'))
        Item_Type=str(request.form.get('Item_Type'))
        Item_MRP=float(request.form.get('Item_MRP'))
        Outlet_Age=float(request.form.get('Outlet_Age'))
        Outlet_Size=str(request.form.get('Outlet_Size'))
        Outlet_Location_Type=str(request.form.get('Outlet_Location_Type'))
        Outlet_Type=str(request.form.get('Outlet_Type'))
        obj=DatabaseConfig()
        return render_template('result.html',data_frame=table_html,results=round(results[0],3))
    
@app.route('/redirect',methods=['POST','GET'])
def redirect11():
    return redirect('/predictdata')
    

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)        