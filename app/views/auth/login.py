from app.views.dashboard.user import user_blueprint
from flask import redirect, render_template, request, flash, jsonify, session
from werkzeug.security import check_password_hash
from ...utils.db.user_queries import UserQueries


@user_blueprint.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    """Log profile in"""

    # Forget any user_id
    if session.get("user_id"):
        flash("You already logged in")
        # Redirect profile to home page
        return redirect("/dashboard/")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Ensure email and password are not empty
        if not email or not password:
            # flash("All fields are required!")
            # return redirect(url_for("profile.login"))
            return jsonify("All fields are required!")

        # Query database by email
        queries = UserQueries()
        # Retrieve a profile by ID
        user = queries.select_user(email=email)

        # Ensure email exists and password is correct
        if not user or not check_password_hash(user.Password, password):
            # flash("invalid email and/or password")
            # return redirect(url_for("profile.login"))

            return jsonify("invalid email and/or password")

        # Remember which profile has logged in
        session["user_id"] = user.UserID

        flash("You were successfully logged in")
        # Redirect profile to home page
        return redirect("/dashboard/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("/auth/login.html")
