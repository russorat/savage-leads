import certifi

DEBUG=True
SECRET_KEY='this is a secret'
#ES_HOSTS=[{'host':'80b5425855de7c733c7848cd71eb4fd0-us-east-1.foundcluster.com',
#           'http_auth':'readwrite:j7fd53ch4fb6fd0bfs',
#           'port':9200,
#           'use_ssl': False}]
ES_HOSTS=[{'host':'80b5425855de7c733c7848cd71eb4fd0.us-east-1.aws.found.io',
           'http_auth':'readwrite:j7fd53ch4fb6fd0bfs',
           'port':9200,#9243,
           'use_ssl': False,#True,
           #'verify_certs': True,
           #'ca_certs':certifi.where()
           'maxsize': 1
          }]
API_BASE='http://savage-leads-api.appspot.com'
SCRIPT_USER_ID='IyTCmeuSDT9rswNGuIxG4giMO9Ni7LUZJeRzPNC8'
SCRIPT_ENCRYPT_KEY='tIlcfzVoZsQEibKZiYQtPmhxu6nTClAIbmdHuhqEgeMio7zlSpwuo3nGQzOH'
