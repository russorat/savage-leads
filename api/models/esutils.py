from elasticsearch import Elasticsearch,RequestsHttpConnection,NotFoundError
from flask import url_for
import config
import json

es = Elasticsearch(config.ES_HOSTS,connection_class=RequestsHttpConnection)

def create(the_data,the_index,the_doc_type):
  try:
    results = es.create(index=the_index,
      doc_type=the_doc_type,
      body=json.dumps(the_data)
    )
    if results['created']:
      return { 'status': 'success',
               'message': '',
               'created_id': results['_id'] }
    else:
      return { 'status': 'failure',
               'message': 'failed to create new record.',
               'created_id': '' }
  except Exception as e:
    print e
    return { 'status': 'failure',
             'message': 'unknown error',
             'created_id': '' }

def update(the_data,primary_key,the_index,the_doc_type):
  old_data = ESUtils.search(size=1,page=0,search='%s:"%s"'%(primary_key,the_data[primary_key]),
                            the_sort=None,the_index=the_index,the_doc_type=the_doc_type)
  if len(old_data['results']) > 0:
    the_data.pop('uri',None)
    the_data.pop('id',None)
    try:
      es.update(index=the_index,
        doc_type=the_doc_type,
        id=old_data['results'][0]['id'],
        body='{ "doc" : %s }'%(json.dumps(the_data))
        )
      return { 'status': 'success',
               'message': '',
               'created_id': old_data['results'][0]['id'] }
    except Exception as e:
      print 'ERROR:',e
      return { 'status': 'failure',
               'message': 'unknown error',
               'created_id': '' }
  else:
    return create(the_data,the_index,the_doc_type)

def delete(the_id,the_index,the_doc_type):
  try :
    es.delete(index=the_index,
      doc_type=the_doc_type,
      id=the_id
    )
    return { 'status': 'success', 'message': '' }
  except NotFoundError as e:
    return { 'status': 'failure', 'message': 'id not found' }
  except Exception as e:
    print e
    return { 'status': 'failure', 'message': 'unknown error' }

def get(the_id,the_index,the_doc_type):
  try:
    results = es.get(
      index=the_index,
      doc_type=the_doc_type,
      id='%s'%(the_id),
      ignore=404
    )
    if results and results['found'] :
      return {'status':'success','message':'','results':[from_es_hit(results)]}
    return {'status':'success','message':'','results':[]}
  except NotFoundError as e:
    return { 'status': 'failure', 'message': 'id not found', 'results': [] }
  except Exception as e:
    print e
    return { 'status': 'failure', 'message': 'unknown exception', 'results': [] }

def search(size,page,search,the_sort,the_index,the_doc_type):
  try:
    results = es.search(
      index=the_index,
      doc_type=the_doc_type,
      size=size,
      q=search or "*",
      sort=the_sort or ""
    )
    retVal = []
    if results and results['hits']['total'] > 0 :
      for hit in results['hits']['hits']:
        retVal.append(from_es_hit(hit))
    return {'status':'success','message':'','results':retVal}
  except Exception as e:
    print e
    return {'status':'failure','message':'unknown error','results':[]}

def from_es_hit(hit):
  the_data = {}
  the_data['id'] = hit['_id']
  for key,val in hit['_source'].items():
    the_data[key] = val
  #the_data['uri'] = url_for('get_'+hit['_index'], id=the_data['id'], _external=True)
  return the_data
