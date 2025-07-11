from flask import Flask, request, render_template, url_for, session, redirect
import ldap
import os
from dotenv import load_dotenv

# Retrieving all .env files
load_dotenv()

app = Flask(__name__)

# Grabs the Secret Key variable from our .env file and initializes it to our Secret Key in Flask config
SECRET_KEY = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# If there is no SECRET_KEY in .env, shoot a runtime error
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set! Set it in the environment.")

LDAP_SERVER = "ldap://localhost"
BASE_DN = "ou=People,dc=vintagestore,dc=com"
LDAP_USER_ATTR = "uid"

# Trigger login function when user connects to the base subdomain (allow the GET and POST methods)
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    
    # IF POST method recieved
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Constructs the full user distinct name based on username
        user_dn = f"{LDAP_USER_ATTR}={username},{BASE_DN}"

        try:
            # Connect and bind with user credentials
            conn = ldap.initialize(LDAP_SERVER)
            conn.simple_bind_s(user_dn, password)
            
            # Store username in session to mark user as logged in
            session['username'] = username

            # Redirect user to the 'welcome' page
            return redirect(url_for('welcome'))
        
        except ldap.INVALID_CREDENTIALS:
            error = "Invalid credentials."
        except ldap.SERVER_DOWN:
            error = "LDAP server is unreachable."

        # Catch any LDAP related exception 
        except Exception as e:
            error = f"LDAP error: {str(e)}"

        # Unbind from LDAP user after use
        finally:
            conn.unbind_s()

    return render_template("login.html", error=error)

# Function for the welcome page
@app.route("/welcome")
def welcome():

    # If username is stored in session, load the welcome page
    if 'username' in session:
        username = session['username']

        # hyperlink reference to logout when logout button is clicked
        return f"<h1>Welcome, {username}!</h1><a href='/logout'>Logout</a>"
    
    # Otherwise redirect to the login function
    else:
        return redirect(url_for('login'))

# Function that triggers when logout button is pressed
@app.route("/logout")
def logout():

    # Clear user session to log out
    session.pop('username', None)
    return redirect(url_for('login'))

# Start server on local device port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
