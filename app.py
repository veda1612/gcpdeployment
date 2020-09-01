# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, render_template, request,redirect
import flask_monitoringdashboard as dashboard
import jsonify
import requests
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
dashboard.bind(app)
app.secret_key = "secret key"
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
model = pickle.load(open('SVC_rbf_model_v1.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('start.html')

@app.route('/',methods = ['POST'])
def start():
    if request.method == 'POST':
        input_type = request.form['input_type']
        if input_type=='single':
            return render_template('index.html')
        elif input_type == 'file':
            return render_template('upload.html')        
        else:
            return redirect('/')
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        else:
            data = pd.read_csv(request.files.get("file"))
            prediction = model.predict(data)
            data['output'] = prediction
            return render_template('simple.html', tables=[data.to_html(classes='data')], titles=data.columns.values)


@app.route("/predict", methods=['POST'])
def predict():    
    if request.method == 'POST':
        Price=request.form['Price']
        if(Price=='low'):
            Price=0                
        elif(Price=='med'):
            Price=1
        elif(Price=='high'):
            Price=2
        else:
            Price=3
        MaintenanceCost=request.form['Maintenance Cost']
        if(MaintenanceCost=='low'):
            MaintenanceCost=0                
        elif(MaintenanceCost=='med'):
            MaintenanceCost=1
        elif(MaintenanceCost=='high'):
            MaintenanceCost=2
        else:
            MaintenanceCost=3
        NumberOfDoors=request.form['Number of Doors']
        if(NumberOfDoors=='5more'):
            NumberOfDoors=5  
        Capacity=request.form['Capacity']
        if(Capacity=='more'):
            Capacity=5            
        SizeOfLuggageBoot=request.form['Size of Luggage Boot']
        if(SizeOfLuggageBoot=='small'):
            SizeOfLuggageBoot=0      
        elif(SizeOfLuggageBoot=='med'):
            SizeOfLuggageBoot=1
        else:
            SizeOfLuggageBoot=2 
        safety=request.form['safety']
        if(safety=='low'):
            safety=0                
        elif(safety=='med'):
            safety=1
        else:
            safety=2
            
        standard_to = StandardScaler()
            
        prediction=model.predict([[Price,MaintenanceCost,NumberOfDoors,Capacity,SizeOfLuggageBoot,safety]])
        output=prediction
        if output<0:
            return render_template('results.html',prediction_texts="Sorry prediction has some problem")
        elif output==0:
            return render_template('results.html',prediction_text= "unaccounted")
        elif output==1:
            return render_template('results.html',prediction_text= "accounted")
        elif output==2:
            return render_template('results.html',prediction_text= "good")
        elif output==3:
            return render_template('results.html',prediction_text= "vgood")
    else:
        return render_template('index.html')



if __name__=="__main__":
    app.run(debug=True)

