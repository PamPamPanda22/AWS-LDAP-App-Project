from flask import Flask, request, render_template
import ldap

app = Flask(__name__)

LDAP_SERVER = "ldap://localhost"
BASE_DN = "ou=People,dc=vintagestore,dc=com"
LDAP_USER_ATTR = "uid"

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Constructs the full user distinct name based on username
        user_dn = f"{LDAP_USER_ATTR}={username},{BASE_DN}"

        try:
            # Connect and bind with user credentials
            conn = ldap.initialize(LDAP_SERVER)
            conn.simple_bind_s(user_dn, password)
            return f"<h1>Welcome, {username}!</h1>"
        except ldap.INVALID_CREDENTIALS:
            error = "Invalid credentials."
        except ldap.SERVER_DOWN:
            error = "LDAP server is unreachable."
        except Exception as e:
            error = f"LDAP error: {str(e)}"

    return render_template("login.html", error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
