from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy

from scraper import *
import pyperclip

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
with app.app_context():
    db = SQLAlchemy(app)
    
class todo(db.Model) : 
    id=db.Column(db.Integer,primary_key=True)
    reference=db.Column(db.String(200),unique=True)
    message=db.Column(db.String(200))
  



def insert_db(ref,msg):
    if 'R' not in ref :
        ref='R'+ref
    row=todo(message=msg,reference=ref)
    if (todo.query.filter(todo.reference == ref).first()) or (' ' in ref):
        pass
    else :
        db.session.add(row)
        db.session.commit()

def delete(id):
    row_to_delete = todo.query.get_or_404(id)
    try:
        db.session.delete(row_to_delete)
        db.session.commit()
    except:
        pass


@app.route('/',methods=['POST','GET'])
def index() : 
    if request.method =='POST' : 
        ref=request.form['input_ref']
        msg=item_det(ref)
        refs=split_ref(ref) 
        pyperclip.copy(msg)
        insert_db(ref,msg)
        rows = todo.query.order_by(todo.id.desc()).all()
        return render_template('home.html',msg=msg,refs=refs,rows=rows)

    else : 
        return render_template('home.html')




if __name__=="__main__" : 
    app.run(debug=True)