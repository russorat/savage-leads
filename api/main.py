import config
from models.esutils import ESUtils
# Import the Flask Framework
from flask import Flask,jsonify,make_response
app = Flask(__name__)
app.config.from_object('config')

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'russ':
      return 'savage'
    return generate_password(username)
    #results = ESUtils.search(1,0,'username:"%s"'%username,'','admin','users')
    #if len(results['results']) > 0:
    #  return results['results'][0]['password']
    #return None

@auth.error_handler
def unauthorized():
  return make_response(
    jsonify({
      'error_message': 'Unauthorized access',
      'results' : []
    }), 401)

@app.errorhandler(404)
def page_not_found(e):
  return make_response(
    jsonify(
      { 'error_message' : 'url not found.',
        'results' : [] }
    ), 404)


@app.errorhandler(500)
def application_error(e):
  return make_response(
    jsonify(
      { 'error_message' : 'unexpected server error.',
        'results' : [] }
    ), 500)

def generate_password(username):
  from hashlib import sha512
  import hmac,datetime
  now = datetime.datetime.now()
  time_str = now.strftime('%Y-%m-%dT%H:%M')
  raw = username+time_str+app.config['SCRIPT_USER_ID']
  hashed = hmac.new(app.config['SCRIPT_ENCRYPT_KEY'], raw, sha512)
  return hashed.hexdigest()

import leads
import settings
import fields
import users
import organizations
