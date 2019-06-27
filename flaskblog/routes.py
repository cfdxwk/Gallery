import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post, Folder
from flask_login  import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/home")
def home():
    #finding all folders belongs to the current user
    folders = Folder.query.filter_by(user_id=current_user.id)
    return render_template('home.html', folders=folders)


@app.route("/about")
def about():
    #just a temporary page
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstname=form.firstname.data,lastname=form.lastname.data, 
            gender=form.gender.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can login now.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture, path):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,path, picture_fn)
    output_size =(125, 125)
    i =Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    #form_picture.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/profile_pics')
            current_user.image_file = picture_file
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.gender = form.gender.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.gender.data = current_user.gender
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form =PostForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.picture.data, 'static/normal_posts')
        post = Post(title= form.title.data, image_file=picture_file, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been Uploaded', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New post', form=form)


@app.route("/all_posts", methods=["GET", "POST"])
@login_required
def all_posts():
    posts = Post.query.filter_by(folder_id=fol_id)
    return render_template('all_posts.html', posts=posts)
