import ssl,json,time,hashlib,certifi
from elasticsearch import Elasticsearch
from google.appengine.api import users
import requests
from requests.auth import HTTPBasicAuth


# Import the Flask Framework
from flask import render_template,request,redirect,session,url_for,flash,g
from flask.ext.login import LoginManager,login_user, logout_user, current_user, login_required
from models.loginForm import LoginForm
from models.registrationForm import RegistrationForm
from models.User import User
from models.Login import Login
from models.Lead import Lead
from main import app

es = Elasticsearch(hosts=app.config['ES_HOSTS'])

@app.route('/settings')
def settings():
  results = requests.get('http://savage-leads-api.appspot.com/api/v1.0/settings',
                         auth=HTTPBasicAuth(g.user.email(), generate_password(g.user.email())))
  if results.status_code == 200:
    return render_template('settings.html',settings=results.json()['results'])
  else:
    return results.text

@app.route('/settings/fields')
@login_required
def settings_fields():
  return render_template('settings_fields.html')

@app.route('/settings/fields/push',methods=['POST'])
@login_required
def add_field():
  tag_list = request.form['tags'].split(',')
  if len(tag_list) > len(g.user.fields) :
    new_field = list(set(tag_list)-set(g.user.fields))
    g.user.add_field(new_field)
  else:
    deleted_fields = list(set(g.user.fields)-set(tag_list))
    g.user.deleted_fields = deleted_fields
  g.user.save()
  return ""
