from main import app,auth
from flask import jsonify,request,abort
import models.esutils as es_utils

@app.route('/api/v1.0/settings', methods=['GET'])
@auth.login_required
def get_settings():
  username = auth.username()
  results = es_utils.search(1,0,'username:"%s"'%username,'',the_index='settings',the_doc_type='settings')
  return jsonify({ 'status': results['status'],
                   'error_message': results['message'],
                   'results': results['results'] })

@app.route('/api/v1.0/settings', methods=['PUT','POST'])
@auth.login_required
def create_settings():
  if not request.json:
    abort(400)
  request.json['username'] = auth.username()
  result = es_utils.update(request.json,'username',the_index='settings',the_doc_type='settings')
  status_code = 200
  if result['status'] == 'success':
    status_code = 201
  return jsonify({ 'status': result['status'],
                   'error_message' : result['message'],
                   'created_id' : result['created_id'] }), status_code
