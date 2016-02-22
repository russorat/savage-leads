import ssl,json,time,hashlib,certifi
from google.appengine.api import users
import requests
from flask import render_template,request,redirect,session,url_for,flash,g,jsonify,abort
from main import app
from main import User
from main import Org

@app.route('/admin',methods=['GET'])
def admin():
  if not g.is_admin:
    abort(401)
  return render_template('admin/admin.html')

@app.route('/admin/list-orgs',methods=['GET'])
def admin_list_orgs():
  if not g.is_admin:
    abort(401)
  orgs = Org.query();
  if not orgs:
    flash('Something went wrong getting orgs.')
    return redirect(url_for('admin'))
  return render_template('admin/admin-list-orgs.html',orgs=orgs)

@app.route('/admin/create-org',methods=['GET'])
def admin_create_org():
  if not g.is_admin:
    abort(401)
  return render_template('admin/admin-create-org.html')

@app.route('/admin/create-org-action',methods=['GET'])
def admin_create_org_action():
  org_id = request.args.get('org_id')
  org_name = request.args.get('org_name')
  org_key = Org(id=org_id,name=org_name).put()
  if not org_key:
    flash('There was an error creating an org.')
    return render_template('admin/admin-create-org.html')
  return redirect(url_for('admin'))

@app.route('/admin/list-users',methods=['GET'])
def admin_list_users():
  if not g.is_admin:
    abort(401)
  users = User.query()
  if not users:
    flash('There was an error getting users')
    return redirect(url_for('admin'))
  return render_template('admin/admin-list-users.html',users=users)

@app.route('/admin/create-user',methods=['GET'])
def admin_create_user():
  if not g.is_admin:
    abort(401)
  return render_template('admin/admin-create-user.html',orgs=Org.query())

@app.route('/admin/create-user-action',methods=['GET'])
def admin_create_user_action():
  org_id = request.args.get('org_id')
  email = request.args.get('email')
  org_key = Org.query(Org.id == org_id).get()
  org_key.member_emails.append(email)
  org_key.put()
  flash('Created user')
  return redirect(url_for('admin'))
