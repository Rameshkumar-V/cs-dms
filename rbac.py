
@app.route("/admin_login",methods=["POST"])
def admin_checker():
    form =  AdminForm()

    if form.validate_on_submit():
        username : str = form.username.data
        password : str = form.password.data
        
        flash('Logged successfully!', 'success')
        return redirect(url_for('add_student'))
    else:
        if form.errors:
            flash('Form contains errors. Please check below.', 'danger')
    
    return render_template('admin_login.html', form=form)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = MyForm()
    form.category.choices=[("1", "Option 1"), ("2", "Option 2"), ("3", "Option 3")]
    
    if form.validate_on_submit():
        roll_no = form.roll_no.data
        dob = form.dob.data
        category = form.category.data
        print("categry : ",category)
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('add_student'))
    else:
        if form.errors:
            flash('Form contains errors. Please check below.', 'danger')
    
    return render_template('index.html', form=form)