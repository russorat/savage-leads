from main import app,auth
from flask import jsonify,request,abort
from models.esutils import ESUtils

@app.route('/api/v1.0/fields', methods=['GET'])
@auth.login_required
def get_fields():
  username = auth.username()
  results = ESUtils.search(1,0,'username:"%s"'%username,'',the_index='settings',the_doc_type='fields')
  return jsonify({ 'status': results['status'],
                   'error_message': results['message'],
                   'results': results['results'] })

@app.route('/api/v1.0/fields/<field_name>', methods=['GET'])
@auth.login_required
def get_field_by_name(field_name):
  username = auth.username()
  results = ESUtils.search(1,0,'username:"%s"'%username,"",the_index='settings',the_doc_type='fields')
  if len(results['results']) > 0:
    field_info = filter(lambda field: field['name'] == field_name, results['results'][0]['fields'])
    return jsonify({ 'status': 'success',
                     'error_message': '',
                     'results': field_info })
  else:
    return jsonify({ 'status': 'failure',
                     'error_message' : 'No fields found for that username'  })


@app.route('/api/v1.0/fields', methods=['PUT','POST'])
@auth.login_required
def add_field():
  if not request.json or \
  'display_name' not in request.json or \
  'name' not in request.json or \
  'type' not in request.json :
    abort(400)
  to_add = { 'display_name': request.json['display_name'],
             'name':request.json['name'],
             'type':request.json['type'],
             'is_deleted':False }
  username = auth.username()
  results = ESUtils.search(1,0,'username:"%s"'%username,"",the_index='settings',the_doc_type='fields')
  if len(results['results']) > 0:
    found_existing = False
    for i in xrange(0,len(results['results'][0]['fields'])):
      field = results['results'][0]['fields'][i]
      if field['name'] == to_add['name']:
        if field['type'] == to_add['type']:
          results['results'][0]['fields'][i]['is_deleted'] = False
          results['results'][0]['fields'][i]['display_name'] = to_add['display_name']
          found_existing = True
          break
        else:
          return jsonify({ 'status': 'failure',
                           'error_message' : 'Field with that name already exists and is a different type.',
                           'created_id' : '' })
    if not found_existing:
      results['results'][0]['fields'].append(to_add)
    result = ESUtils.update(results['results'][0],'username',the_index='settings',the_doc_type='fields')
  else:
    new_fields = { 'username': username,
                   'fields' : [to_add] }
    result = ESUtils.update(new_fields,'username',the_index='settings',the_doc_type='fields')
  status_code = 200
  if result['status'] == 'success':
    status_code = 201
  return jsonify({ 'status': result['status'],
                   'error_message' : result['message'],
                   'created_id' : result['created_id'] }), status_code

@app.route('/api/v1.0/fields/<field_name>', methods=['DELETE'])
@auth.login_required
def delete_field(field_name):
  username = auth.username()
  results = ESUtils.search(1,0,'username:"%s"'%username,"",the_index='settings',the_doc_type='fields')
  if len(results['results']) > 0:
    for i in xrange(0,len(results['results'][0]['fields'])):
      if results['results'][0]['fields'][i]['name'] == field_name:
        results['results'][0]['fields'][i]['is_deleted'] = True
        break
    #results['results'][0]['fields'] = filter(lambda field: field['name'] != field_name, results['results'][0]['fields'])
    result = ESUtils.update(results['results'][0],'username',the_index='settings',the_doc_type='fields')
    return jsonify({ 'status': result['status'],
                     'error_message' : result['message']  })
  else:
    return jsonify({ 'status': 'failure',
                     'error_message' : 'No fields found for that username'  })
