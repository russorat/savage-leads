import ssl,json,time,hashlib,certifi
from elasticsearch import Elasticsearch
from google.appengine.api import users


# Import the Flask Framework
from flask import render_template,request,redirect,session,url_for,flash,g
from flask.ext.login import LoginManager,login_user, logout_user, current_user, login_required
from models.loginForm import LoginForm
from models.registrationForm import RegistrationForm
from models.User import User
from models.Login import Login
from models.Lead import Lead
from main import app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
es = Elasticsearch(hosts=app.config['ES_HOSTS'])

@app.route('/login', methods=['GET', 'POST'])
def login():
  flash('Already logged in with Email="%s"'%g.user.email())
  return redirect(request.args.get('next') or url_for('main'))

@app.route('/leads')
def leads():
  #columns = g.user.get_undeleted_fields()
  #data = Lead.get_leads(g.user.id)
  return render_template('leads.html',columns=[],data=[])

@app.route('/leads/new',methods=['GET', 'POST'])
@login_required
def add_lead():
  if request.method == 'POST':
    create_lead(request.form)
    flash('Currently indexing the lead. You may need to refresh to see it.')
  return redirect(url_for('leads'))

@app.route('/leads/delete')
@login_required
def delete_lead():
  owner_id = request.values.get('owid')
  email = request.values.get('email')
  delete_lead(owner_id,email)
  time.sleep(1) #wait for es to index
  return redirect(url_for('leads'))
