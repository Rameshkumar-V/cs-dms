# FLASK
from flask import Flask,render_template,flash,redirect,url_for,request
from flask import abort
from flask import session
# ADMIN
from admin import *
# DATABASE
from database import db
from database import *
from functools import wraps
# form
from login_form import MyForm,AdminForm,DiscussionForm
# Bootstrap
from flask_bootstrap import Bootstrap


app : Flask = Flask(__name__,template_folder="template")

app.secret_key = "djdjdjdjdjjdjdj"
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing other apps
admin.init_app(app)
db.init_app(app)
login_manager.init_app(app)
Bootstrap(app)




@app.route("/")
def Home():
    return redirect(url_for("user_sign_in"))
    return "Welcome to our Application"
"""
 SIGN UP :
    1) For students
    DESCRIPTION :
        * User signup using username like roll no and password with Date of birth.
"""
@app.route("/user/signup", methods=['GET', 'POST'])
def user_sign_in():
    
    form = MyForm()
    category_coice =  db.session.query(Category.c_id,Category.category).all()
    form.category.choices = form.category.choices = list(map(lambda x: (str(x.c_id), x.category), category_coice)) if category_coice else None

    if form.validate_on_submit():
        user : User = User(
            username=form.roll_no.data,
            dob=form.dob.data,
            role="user",
            category_id= int(form.category.data)
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash("Sign Up Success",'success')
            return redirect(url_for("user_login"))
            
        except:
            db.session.rollback()
            flash("Sign Up Failed !,User Exists")
            return redirect(url_for("user_sign_in"))
            
    
    
    return render_template("forms/user_login.html", form=form,title="Sign Up")
    
    
    
"""
 LOGIN :
    1) For students
    DESCRIPTION :
        * User login using username like roll no and password with Date of birth.
"""
@app.route("/user/login", methods=['GET', 'POST'])
def user_login():
    form = MyForm()
    category_coice =  db.session.query(Category.c_id,Category.category).all()
    form.category.choices = form.category.choices = list(map(lambda x: (str(x.c_id), x.category), category_coice)) if category_coice else None

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.roll_no.data,dob=form.dob.data,category_id=form.category.data).first()
        try:
            if user :       
                login_user(user)
                session['user_type'] = 'user'
                flash('Logged in successfully.')
                return redirect(url_for('student_topic_selection', category=user.category_id))
            else: 
                flash('Invalid roll number or user does not exist.')
        except:
            return redirect(url_for("user_login"))

    return render_template("forms/user_login.html", form=form,title="Log In")


def required_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('user_type',None)==str(role):
                return f(*args, **kwargs)
            else:
                # Return a 404 or redirect as per your application's needs
                return abort(404)
        return decorated_function
    return decorator


    
@app.route("/admin/login", methods=['GET', 'POST'])
def login_admin():
    form =AdminForm()
    if form  and form.validate_on_submit():
            admin= Admin.query.filter_by(username=form.username.data,password=form.password.data).first()
            if admin:
                session['user_type'] = 'admin'
                login_user(admin)
                flash("Logged In ")
                return redirect("/admin")
                
    return render_template("forms/admin_login.html", form=form,url="/admin/login")
    
"""
    TOPICS :
        * In Topics page showing topics assigned to the user by admin.
"""
@app.route("/topics", methods=['GET'])
@login_required
@required_role("user")
def student_topic_selection():

    category_id  : int = int(current_user.category_id)
    is_accessible : SQLAlchemy = db.session.query(User).filter(User.id==current_user.id,User.category_id==category_id).first()

    if  not is_accessible:
        return {
            "message" : "Your not Have to access this resources."
        }
        
    topics = db.session.query(Discussion.id,Discussion.title,Discussion.created_date).filter(Discussion.category_id==category_id,Discussion.is_visible==True).all()
    if topics:
        convert_dict = list(
        map(
            lambda x : dict(zip(('id','title','created_date'),x)),topics
            )
        )
    else:
        convert_dict = None
  
    return render_template("topic_selection.html",topics=convert_dict)


"""
    DISCUSSION :
        * In this page input from user about their  discussion about topic.
        * Checking discussion exists
        * Checking is access to this topic
        * Checking Student already Submited their Remarks
        
"""

@app.route("/disscusion/<id>", methods=['GET', 'POST'])
@required_role("user")
def user_disscussion(id):
    
    category_id  : int = int(current_user.category_id)
    discussion  = db.session.query(Discussion).filter(Discussion.id==id,Discussion.category_id==category_id).first()
    print("Discussion_:",discussion)

    student_remarks = db.session.query(StudentRemarks).filter(StudentRemarks.discussion_id==discussion.id).first()

    is_accessible = discussion if discussion else None
    if  not is_accessible:
        return {
            "message" : "Your not Have to access this resources."
        }
        
    if student_remarks:
        form = DiscussionForm(vote=student_remarks.is_accept,remarks=student_remarks.remarks)
    else:   
        form = DiscussionForm()
    
    if form.validate_on_submit():
        
        discussion = StudentRemarks(
            discussion_id = discussion.id,
            student_id = current_user.id,
            is_accept = True if form.vote.data else False,
            remarks = form.remarks.data      
        )
        try:
            if student_remarks:
                student_remarks.is_accept= True if form.vote.data else False
                student_remarks.remarks= form.remarks.data   
            else:
                db.session.add(discussion)          
        except Exception as e:
            db.session.rollback()
            pass
        finally:
            db.session.commit()
        return "Your Discussion Submitted"
    return render_template("forms/discussion_form.html",form=form,title="Discussion Form",topic=discussion.title)


@app.route("/logout")
def logout():
    logout_user()
    

@app.route("/build")
def build():
    with app.app_context():
        db.create_all()
        db.session.add(User(username="qwert",dob=date(2024, 8, 12),role="student",category_id=1))
        db.session.add(Admin(username="admin@sm",password="12345678"))
        db.session.commit()
    return "db constructed"
    
    


from datetime import date
if __name__=='__main__':

    with app.app_context():
        db.create_all()
        db.session.add(User(username="qwert",dob=date(2024, 8, 12),role="student",category_id=1))
        db.session.commit()
    print('user created')
    
    app.run(debug=True)






    
    
    