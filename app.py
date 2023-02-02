from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from scraper import *
import pyperclip

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

@app.route('/',methods=['POST','GET'])
def index() : 
    if request.method =='POST' : 
        ref=request.form['input_ref']
        msg=item_det(ref)
        refs=split_ref(ref) 
        pyperclip.copy(msg)
        return render_template('home.html',msg=msg,refs=refs)
    else : 
        return render_template('home.html')


if __name__=="__main__" : 
    app.run(debug=True)