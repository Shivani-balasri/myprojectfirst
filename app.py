from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import random





from datetime import datetime
from rtrt import rr

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow) 
    no = db.Column(db.Integer)  
    
    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/', methods=['POST','GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content']
        a=rr(task_content)
        new_task = Todo(content=task_content , no=a)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding ur  task'
        
        
    else: 
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deletig'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task= Todo.query.get_or_404(id)
    
    if request.method=='POST':
        task.content=request.form['content']
        a=rr(task.content)
        task.no=a
        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return 'there is an isuse while update'
    
    

    else:
        return render_template('update.html',task=task)
    
if __name__=="__main__":
    app.run(debug=True)
    
    
    
