from flask import Flask, request, render_template, redirect
from config import Config
import requests
from api import API
from urllib import parse
import jwt

app = Flask(__name__)

# Simple flask app to provide JWT authorization to DirectAdmin
# Requires: Flask, requests


@app.route('/')
def hello_world():
    return Config.hello_world_text


@app.route('/auth/da', methods=["GET", "POST"])
def da_auth():
    if request.method == "GET":
        # Return base login template (for DA)
        return render_template("da_login.html")

    # If the request was not GET, it must be POST, therefore we can continue
    user_username = request.form.get("username")
    user_password = request.form.get("password")
    user_redirect = request.form.get("redirect")

    # Verify all elements are present
    if [x for x in (user_username, user_password, user_redirect) if x is None]:
        return render_template("da_login.html", pageError="Your request did not contain all of the needed elements, please try again", returnValue=user_redirect), 400

    # Verify return URL, prevent redirect attack
    if parse.urlparse(user_redirect).netloc not in Config.authorized_redirects:
        return render_template("da_login.html", pageError="Your request attempted to redirect to an invalid URL", returnValue=user_redirect), 400

    # Attempt login using provided elements
    req1 = requests.post(Config.da_url + "/CMD_LOGIN", data={'username': user_username, 'password': user_password, 'json': 'yes'})
    # Check if DA Login actually worked
    if req1.status_code == 401:
        return render_template("da_login.html", pageError="Invalid username or password. Please try again", returnValue=user_redirect)

    # If DA Login was successful, setup DA API to ask for user's email
    api = API(username=Config.username, password=Config.pwd, server=Config.da_url)

    # Ask DA API for user's configuration
    req2 = api.cmd_api_show_user_config({'user': user_username})
    # Extract email from user configuration
    email = req2.get("email")[0]

    # Encode user data into JWT
    encoded_info = jwt.encode({'id': user_username, 'name': user_username, 'email': email}, Config.encode_pwd, algorithm='HS256')

    # Determine how to send user back to the app
    base_url = parse.unquote_plus(user_redirect)

    # This seemingly random and ugly check is useful in the case of extra parameters being present
    # In our case this was DeskPRO adding a debug parameter when we were testing the app
    if "?" in base_url:
        url = base_url + "&jwt=" + parse.quote_from_bytes(
            encoded_info)
    else:
        url = base_url + "?jwt=" + parse.quote_from_bytes(
            encoded_info)

    return redirect(url)


@app.route('/auth/blesta')
def blesta_auth():
    # TODO: Write Blesta implementation
    return 'Not Implemented.'


if __name__ == '__main__':
    # It is recommended to run this application under Gunicorn or another WSGI server
    # (we use Gunicorn with success in our deployment)
    # DO NOT USE THE FLASK DEBUG SERVER IN PRODUCTION!
    app.run()
