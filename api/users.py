from main import app,auth
from flask import jsonify,request,abort
import models.esutils as es_utils

@app.route('/api/v1.0/users', methods=['GET'])
@auth.login_required
def get_all_users():
  search = request.args.get('q') or None
  results = es_utils.search(1000,0,search,the_sort='',the_index='admin',the_doc_type='users')
  return jsonify({ 'status': results['status'],
                   'error_message': results['message'],
                   'results': results['results'] })

@app.route('/api/v1.0/users', methods=['POST'])
@auth.login_required
def create_user():
  if auth.username() != 'russ':
    abort(400)
  if not request.json or 'username' not in request.json:
    abort(400)
  to_add = { 'username' : request.json['username'],
             'org_id' : request.json['org_id'],
             'access_token' : generate_password(request.json['username']) }
  result = es_utils.update(to_add,'username',the_index='admin',the_doc_type='users')
  status_code = 200
  if result['status'] == 'success':
    status_code = 201
  return jsonify({ 'status': result['status'],
                   'error_message' : result['message'],
                   'created_id' : result['created_id'] }), status_code

def generate_password(username):
  from hashlib import sha512
  import hmac,datetime
  now = datetime.datetime.now()
  time_str = now.strftime('%Y-%m-%dT%H:%M')
  raw = username+time_str+app.config['SCRIPT_USER_ID']
  hashed = hmac.new(app.config['SCRIPT_ENCRYPT_KEY'], raw, sha512)
  return hashed.hexdigest()
