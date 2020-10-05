import logging.config

import os
from flask import Flask, Blueprint, url_for, session, redirect
from rest_api_demo import settings
from rest_api_demo.api.blog.endpoints.posts import ns as  blog_posts_namespace 
from rest_api_demo.api.blog.endpoints.categories import ns as blog_categories_namespace
from rest_api_demo.api.restplus import api
from rest_api_demo.database import db
# Integrate security
from authlib.integrations.flask_client import OAuth
# decorator for routes that should be accessible only by logged in users
from auth_decorator import login_required
from datetime import timedelta


app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

# set oauth to the app
oauth = OAuth(app)

# Set oAuth Register for Google
google = oauth.register(
    name='google',
    client_id='917119924009-80eq2p27e8096ne7ecccmuvh08l3hbkv.apps.googleusercontent.com',
    client_secret='yaHRsURbCudieEReNCARfZSP',
    access_token_url='http://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='http://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
@login_required
def hello_world():
    email = dict(session)['profile']['email']
    return f'iepa, iepa !!! you are logged in as {email}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')    
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')    
    token = google.authorize_access_token()
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    print(resp)
    user_info = resp.json()
    print(user_info)
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # do something with the token and the profile
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/api')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['SECRET_KEY'] = settings.SECRET_KEY
    # set cookie for oauth session
    flask_app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
    flask_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    api.add_namespace(blog_categories_namespace)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
