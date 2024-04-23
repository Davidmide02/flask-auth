from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db =SQLAlchemy(app)

app.secret_key = 'mySecretKey'

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'




@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else: 
        return render_template('index.html')


@app.route('/register', methods= ['POST', 'GET'])
def register():
    if request.method =='POST': 
     username = request.form.get('username')
     password = request.form.get('password')
     age = request.form.get('age')

     new_user = User(username = username, age = age)
     new_user.set_password(password) # Hash password before saving
     db.session.add(new_user)
     db.session.commit()
     session['username'] = username
     print("Register successfully")
     return redirect(url_for('index'))
    
    else: 
       return render_template('register.html')
   


@app.route('/login', methods= ['POST', 'GET'])
def login():
    if request.method =='POST':
     username = request.form.get('username')
     password = request.form.get('password')
     user = User.query.filter_by(username=username).first()
     if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('index'))
     else:
         return render_template('login.html', err="Error credentials, login again")
        

    else: 
        return render_template('login.html')
    #  if username and User.check_password(password):
    #      return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))




if __name__== "__main__":
    app.run(debug=True)

    # register page
    # login page
    # welcome page