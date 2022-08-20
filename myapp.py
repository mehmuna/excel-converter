from flask import Flask, render_template,send_file,redirect,url_for,send_from_directory,abort
from flask import request
import os
from io import BytesIO
from flask import jsonify
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_httpauth import HTTPDigestAuth
import os
import sys
sys.path.append('D:\OCRproject_Final')
from main import pdf_to_excel
from openpyxl import load_workbook
import glob

import requests





#webserver gateway interface
app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
    "daud": "007",
    "khan": "005"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None



BASE_PATH=os.getcwd()
UPLOAD_PATH=os.path.join(BASE_PATH,'static/upload/')

@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = r"D:\OCRproject_01\outPut_usecase5\1.xlsx"
    return send_file(path, as_attachment=True)






@app.route ('/',methods=['POST','GET'])
@auth.login_required
def index():
    if request.method=='POST':
        upload_file=request.files['file']
        filename=upload_file.filename
        path_save=os.path.join(UPLOAD_PATH,filename)
        print ("this is path of upload image ..........",path_save)
        #file_list=(glob.glob(r"static/upload/*.pdf"))
        #print("this is path to file_list",file_list)
        upload_file.save(path_save)
        print(path_save)
        file_list=(glob.glob(r"static/upload/*.pdf"))
        print("this is path to file_list",file_list)
        pdf_to_excel(file_list)
       # return render_template('layout1.html',)
    
        os.remove(path_save)
        
        
    return render_template('layout1.html',)
        #main_func()

    return render_template("layout1.html")




    # Boilerplate code
if __name__ =="__main__":
    app.run(debug=True)


    

