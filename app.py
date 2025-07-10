from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Dummy user/password for now
VALID_USERS = {
    "jdoe": "password123"
}

# Defines when function triggers and allowed methods 
@app.route("/", methods=["GET", "POST"]) 
def login():
    error = None
    # If POST method is submitted from user
    if request.method == "POST":

        # Username and password stored from HTML form
        username = request.form["username"] 
        password = request.form["password"]

        # Checks if password from form matches the username
        if username in VALID_USERS and VALID_USERS[username] == password:
            #return new html page
            return f"<h1>Welcome, {username}!</h1>"
        else:
            error = "Invalid username or password."

    #return page from login.html with error if applicable
    return render_template("login.html", error=error)

# Starts the Flask development server, listening on all network interfaces (0.0.0.0) at port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
