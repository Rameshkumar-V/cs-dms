import datetime
topics = [('AAAAA', datetime.datetime(2024, 9, 12, 18, 22, 29))]
conver_dict = list(
    map(
        lambda x : dict(zip(("title","date"),x)),topics
        )
    )
print(conver_dict)

print(list(conver_dict))

 topics = [
        {
            
            'title' : "Symposium Discussion",
            'created_date' : "1-2-2020 mon"
            
        }
    ]
    
    
    note user means student
    
    class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date)
    role = db.Column(db.String(10), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.c_id'))
    
    
    class StudentRemarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False) # do relationship with student object
    is_accept = db.Column(db.Boolean, nullable=False)
    remarks = db.Column(db.Text)