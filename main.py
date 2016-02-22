from google.appengine.api import users
from models.user import User
from models.org import Org
from google.appengine.ext import ndb
import api.leads as leads_api

from flask import Flask,jsonify,make_response,g,redirect,url_for,render_template,request,abort
app = Flask(__name__)
app.config.from_object('config')

@app.before_request
def before_request():
  g.user = users.get_current_user()
  if not g.user:
    login_url = users.create_login_url(request.args.get('next') or url_for('main'))
    return render_template('login.html',
                          link=login_url)
  g.is_admin = users.is_current_user_admin()
  g.logout_url = users.create_logout_url('/')
  g.org = Org.query(Org.members == g.user.user_id()).get()
  if not g.is_admin:
    sl_user = ndb.Key(User,g.user.user_id()).get()
    if not sl_user:
      return first_time()

@app.route('/')
def main():
  return render_template('main.html')

@app.route('/leads')
def leads():
  leads = get_leads(1000,0,'*')
  return render_template('leads.html',leads=leads)

@app.errorhandler(401)
def unauthorized(e):
  return render_template('errors/401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
  return 'Sorry, unexpected error: {}'.format(e), 500

def first_time():
  orgs = Org.query(Org.member_emails == g.user.email()).get()
  if not orgs:
    return render_template('no-org.html')
  orgs.members.append(g.user.user_id())
  orgs.put()
  User(id=g.user.user_id()).put()
  g.org = orgs
  return render_template('register.html',org=orgs.name)

import settings.views
import admin.views
