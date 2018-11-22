from flask import render_template,redirect,url_for,abort
from ..models import User,Blog,Comment,Subscriber
from .forms import UpdateProfile,BlogForm,CommentForm,SubscriberForm
from . import main
from ..import db,photos
from flask_login import login_required,current_
User
from datetime import datetime
from ..email import mail_message



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

        return render_template("profile/profile.html",user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
        return render_template('profile/update.html',form=form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
        return redirect(url_for('main.profile',unmae=uname))

@main.route('/fashion', methods=['GET','POST'])
@login_required
def fashion():
    blog_form=BlogForm()
    if blog_form.validate_on_submit():        
        fashion = Blog(category=blog_form.category.data,title = blog_form.title.data)
        db.session.add(fashion)
        db.session.commit()
    subscribers = Subscriber.query.all()
    for email in subscribers:
        mail_message("Welcome To My Blog Site ","email/welcome_post",email.email,subscribers=subscribers)
    return render_template('fashion.html',blog_form=blog_form) 



@main.route('/', methods=['GET','POST'])
def subscriber():
    subscriber_form=SubscriberForm()
    if subscriber_form.validate_on_submit():
        subscriber= Subscriber(email=subscriber_form.email.data,title = subscriber_form.title.data)
        db.session.add(subscriber)
        db.session.commit()
        mail_message("Welcome To My Blog Site ","email/welcome_subscriber",subscriber.email,subscriber=subscriber)
    subscriber = Blog.query.all()
    fashion = Blog.query.all()
    return render_template('index.html',subscriber=subscriber,subscriber_form=subscriber_form,fashion=fashion) 

@main.route('/comments/<int:id>', methods=['GET','POST'])
def comment(id):
    comment_form=CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(description=comment_form.description.data,blog_id=id)
        db.session.add(new_comment)
        db.session.commit()
    comments = Comment.query.filter_by(blog_id=id)
    return render_template('comment.html',comment_form=comment_form,comments=comments)    
