from main import app,auth
from flask import jsonify,request,abort
from models.esutils import ESUtils


@app.route('/api/v1.0/organizations', methods=['GET'])
@auth.login_required
def get_all_orgs():
  search = request.args.get('q') or None
  results = ESUtils.search(1000,0,search,the_sort='',the_index='admin',the_doc_type='orgs')
  return jsonify({ 'status': results['status'],
                   'error_message': results['message'],
                   'results': results['results'] })


@app.route('/api/v1.0/organizations', methods=['POST','PUT'])
@auth.login_required
def create_org():
  if not request.json or not 'name' in request.json:
    abort(400)
  result = ESUtils.update(request.json,'name',the_index='admin',the_doc_type='orgs')
  status_code = 200
  if result['status'] == 'success':
    status_code = 201
  return jsonify({ 'status': result['status'],
                   'error_message' : result['message'],
                   'created_id' : result['created_id'] }), status_code

@app.route('/api/v1.0/organizations/<org_id>', methods=['GET'])
@auth.login_required
def get_org(org_id):
  results = ESUtils.get(id,the_index='admin',the_doc_type='orgs')
  return jsonify({ 'status': results['status'],
                   'error_message': results['message'],
                   'results': results['results'] })

@app.route('/api/v1.0/organizations/<org_id>', methods=['DELETE'])
@auth.login_required
def delete_org(org_id):
  result = ESUtils.delete(org_id,the_index='admin',the_doc_type='orgs')
  return jsonify({ 'status': result['status'],
                   'error_message' : result['message']  })
