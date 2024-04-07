from flask import Blueprint, render_template, request, flash,redirect, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from social_media import youtube



views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html",user=current_user)


@views.route('/results',methods=['GET','POST'])
@login_required
def results():
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link') 
        # flash(youtube_link+">>>>>>>>>>>>.youtube link")
        # youtube_link = request.form.get('youtube_link')s
    data = {}  # Initialize an empty dictionary for each new request
    result = youtube.link(youtube_link)
    # flash(result)
    youtube_link=""

    
    if result:
        # flash(result)
        data = result
    
    return render_template("results.html",you=youtube_link,data=data,user=current_user)
    # return render_template('home.html',user=current_user)


