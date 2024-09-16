from flask import Flask, url_for, redirect, abort
from functools import wraps
from flask_admin import Admin, AdminIndexView,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_required,login_user,logout_user,UserMixin
from database import db, User, Category,StudentRemarks,Discussion  # Ensure these are correctly imported from your database module
from database import Admin as db_admin
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a real secret key

from flask import session
# Initialize login manager
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(id):
    if 'user_type' in session:
        print("seesion found ")
        user_type = session['user_type']
        print(user_type)
        if user_type == 'user':
            user = User.query.get(int(id))
    
            if user:
                return user
        if user_type == 'admin':
            print("Admin ivaruh")
            admin = db_admin.query.get(int(id))
            print("data = ",admin)
    
            if admin:
                return admin

# RE CONFIGURE MODELVIEW
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_form'))
    
from wtforms_sqlalchemy.fields import QuerySelectField # type: ignore

class MyDiscussion(ModelView):
    form_columns = ('title', 'category','is_visible')
    
    form_extra_fields = {
        'category': QuerySelectField('Category', query_factory=lambda: Category.query, get_label=lambda x: x.category)
    }
class MyStudentRemarks(ModelView):
    column_list = ['student_id','is_accept','remarks']
    can_edit = False

from sqlalchemy import func,case
from sqlalchemy import func, case

class MyDiscussionReview(BaseView):
    @expose("/")
    def index(self):
        title = "Discussion Review"

        # Calculate total remarks, positive and negative remarks grouped by discussion ID
        total_discussion = db.session.query(
            StudentRemarks.discussion_id,
            func.count(StudentRemarks.id).label('total_remarks'),
            func.sum(case((StudentRemarks.is_accept == True, 1), else_=0)).label('positive_remarks'),
            func.sum(case((StudentRemarks.is_accept == False, 1), else_=0)).label('negative_remarks')
        ).group_by(StudentRemarks.discussion_id).all()

        # Prepare the discussion details with counts
        discussion_details = []
        for discussion in total_discussion:
            total = discussion.total_remarks
            positive = discussion.positive_remarks
            negative = discussion.negative_remarks
            success_percentage = (positive / total) * 100 if total > 0 else 0
            failure_percentage = (negative / total) * 100 if total > 0 else 0
            
            result = "POSTIVE" if success_percentage>=failure_percentage else "NEGATIVE"

            discussion_details.append({
                'discussion_id': discussion.discussion_id,
                'total': total,
                'positive': positive,
                'negative': negative,
                'success_percentage': success_percentage,
                'failure_percentage': failure_percentage,
                'result' : result
            })

        return self.render('admin/discussion_review.html',
                           title=title,
                           discussion_details=discussion_details)

class MyAdminIndexView(AdminIndexView):
    
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
    
    
    
    @login_required
    @required_role("admin")
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_form'))


admin = Admin(app, name='Dashboard', template_mode='bootstrap3',index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Category, db.session))
admin.add_view(MyDiscussion(Discussion, db.session))
admin.add_view(MyStudentRemarks(StudentRemarks, db.session))
admin.add_view(MyDiscussionReview(name="Discussion Review", endpoint="discussion_review"))



@app.errorhandler(403)
def forbidden_error(error):
    return "You don't have permission to access this page.", 403


