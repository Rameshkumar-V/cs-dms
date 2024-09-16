from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, UserMixin
import os
from datetime import datetime
app = Flask(__name__)


# CONFIGURATIONS
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# os.getenv('DATABASE_URL')


app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///db.db"
db = SQLAlchemy()



class Admin(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False,unique=True)
    dob = db.Column(db.Date)
    role = db.Column(db.String(10), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.c_id'))

# CATEGORY MODEL
class Category(db.Model):
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(30), unique=True, nullable=False)
    discussions = db.relationship("Discussion", backref="discussion_category", lazy=True)

    def __repr__(self):
        return f"Category('{self.category}')"


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.c_id'))
    category = db.relationship("Category", lazy=True)
    is_visible = db.Column(db.Boolean, nullable=False)
    student_remarks = db.relationship("StudentRemarks", back_populates="discussion")




class StudentRemarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_accept = db.Column(db.Boolean, nullable=False)
    remarks = db.Column(db.Text)
    discussion = db.relationship("Discussion", back_populates="student_remarks")
    

  

    
    
    