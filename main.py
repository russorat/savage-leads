import ssl,json,time,hashlib
from elasticsearch import Elasticsearch

# Import the Flask Framework
from flask import Flask
from flask import render_template,request,redirect,session,url_for,flash,g
from flask.ext.login import LoginManager,login_user, logout_user, current_user, login_required
from models.loginForm import LoginForm
from models.registrationForm import RegistrationForm
from models.User import User
from models.Login import Login

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='this is a secret'
)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.before_request
def before_request():
  g.user = current_user

@app.route('/')
def main():
  return render_template('main.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if g.user is not None and g.user.is_authenticated():
    flash('Already logged in with Email="%s"'%g.user.email)
    return redirect(url_for('main'))
  form = RegistrationForm()
  if form.validate_on_submit():
    if User.get_from_email(form.email.data):
      flash('Sorry, that email address is already in use.')
    else:
      login = Login()
      login.email = form.email.data
      login.set_pass_from_hashed_pass(form.password.data)
      login.save()
      login = None
      user = User()
      user.email = form.email.data
      user.save()
      user = User.get(user.id)
      login_user(user, remember = False)
      flash('Registration successful for email:"%s"'%user.email)
      return redirect(request.args.get('next') or url_for('main'))
  return render_template('register.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if g.user is not None and g.user.is_authenticated():
    flash('Already logged in with Email="%s"'%g.user.email)
    return redirect(url_for('main'))
  form = LoginForm()
  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data
    if Login.try_login(form.email.data, form.password.data):
      user = User.get_from_email(form.email.data)
      login_user(user, remember = session['remember_me'])
      session.pop('remember_me', None)
      return redirect(request.args.get('next') or url_for('main'))
    else:
      flash('Login failed with Email="%s"'%form.email.data)
  return render_template('login.html',form=form)

@login_manager.user_loader
def load_user(id):
  return User.get(id)

@app.route('/logout', methods=['GET'])
def logout():
  logout_user()
  flash('Logged out.')
  return redirect(url_for('main'))

@app.route('/leads')
@login_required
def leads():
  columns = []
  data = []
  results = get_es_leads()
  if(get_results_count(results) > 0):
    data = results['hits']['hits']
    columns = find_all_columns(results['hits']['hits'])
  return render_template('leads.html',columns=columns,data=data)

@app.route('/leads/new',methods=['GET', 'POST'])
@login_required
def add_lead():
  if request.method == 'POST':
    create_lead(request.form)
    time.sleep(1) #wait for es to index
  return redirect(url_for('leads'))

@app.route('/leads/delete/<lead_id>')
@login_required
def delete_lead(lead_id):
  delete_lead(lead_id)
  time.sleep(1) #wait for es to index
  return redirect(url_for('leads'))

@login_manager.user_loader
def load_user(userid):
  return User.get(userid)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return 'Sorry, unexpected error: {}'.format(e), 500


def delete_lead(id):
  es = Elasticsearch()
  return es.delete(
    index='leads',
    doc_type='leads',
    id=id
  )

def create_lead(data):
  es = Elasticsearch()
  return es.create(
    index='leads',
    doc_type='leads',
    body=json.dumps(data)
  )

def get_es_leads():
  es = Elasticsearch()
  return es.search(
    index='leads',
    doc_type='leads',
    size=1000,
    sort='last_name:ASC,first_name:ASC'
  )

def get_results_count(result):
  return result['hits']['total']

def find_all_columns(hits):
  columns = []
  for hit in hits:
    source = hit['_source']
    keys = list(set(columns + source.keys()))
    keys.sort()
    columns = keys
  return columns
