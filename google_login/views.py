import json
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user, login_user
from google_login.models import User, db
from google_login.utils import get_google_provider_cfg
from google_login import create_app
from oauthlib.oauth2 import WebApplicationClient
import requests

views = Blueprint('views', __name__)


@views.route("/")
def home():
    if current_user.is_authenticated:
        return "Welcome Home"
    return "Please login"


@views.route("/google-login")
def google_login():
    from google_login import create_app
    app = create_app()
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    # OAuth 2 client setup
    client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@views.route("/google-login/callback")
def callback():
    from google_login import create_app
    app = create_app()
    # Get authorization code Google sent back to you
    client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config['GOOGLE_CLIENT_ID'],
              app.config['GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        email = userinfo_response.json()["email"]
        last_name = userinfo_response.json()["family_name"]
        first_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            firstnames=first_name,
            surname=last_name,
            email=email,
            password="testing321"
        )
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for("views.home"))
