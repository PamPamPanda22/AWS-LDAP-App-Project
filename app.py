from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

# Set a secret key for session management (use a strong random key in production)
app.config['SECRET_KEY'] = 'replace-this-with-a-secure-random-key'

# Dummy user/password for now
VALID_USERS = {
    "jdoe": "password123"
}

@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in VALID_USERS and VALID_USERS[username] == password:
            # Store username in session to mark user as logged in
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/welcome")
def welcome():
    # Check if user is logged in by looking for 'username' in session
    if 'username' in session:
        username = session['username']
        return f"<h1>Welcome, {username}!</h1><a href='/logout'>Logout</a>"
    else:
        # Not logged in, redirect to login page
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    # Clear user session to log out
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)