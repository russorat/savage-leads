from flask import jsonify,request,abort
from models.esutils import ESUtils

def get_leads(size,page,search):
  results = ESUtils.search(size,page,search,the_sort='email:ASC',the_index='leads',the_doc_type='leads')
  return { 'status': results['status'],
           'error_message': results['message'],
           'results': results['results'] }


def create_lead():
  if not request.json or not 'email' in request.json:
    abort(400)
  result = ESUtils.update(request.json,'email',the_index='leads',the_doc_type='leads')
  status_code = 200
  if result['status'] == 'success':
    status_code = 201
  return jsonify({ 'status': result['status'],
                   'error_message' : result['message'],
                   'created_id' : result['created_id'] }), status_code

def update_lead():
  if not request.json or not 'email' in request.json:
    abort(400)
  result = ESUtils.update(request.json,'email',the_index='leads',the_doc_type='leads')
  status_code = 200
  if result['status'] == 'success':
    status_code = 201
  return jsonify({ 'status': result['status'],
                   'error_message' : result['message'],
                   'created_id' : result['created_id'] }), status_code

def get_leads(id):
  results = ESUtils.get(id,the_index='leads',the_doc_type='leads')
  return jsonify({ 'status': results['status'],
                   'error_message': results['message'],
                   'results': results['results'] })

def delete_lead(lead_id):
  result = ESUtils.delete_lead(lead_id,the_index='leads',the_doc_type='leads')
  return jsonify({ 'status': result['status'],
                   'error_message' : result['message']  })
