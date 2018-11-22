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
