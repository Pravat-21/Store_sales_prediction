from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.prediction_pipeline import CustomData,PredictPipeline

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
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
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('result.html',results=round(results[0],3))
    

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)        