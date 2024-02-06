from flask import redirect, session
from app.views.dashboard.user import user_blueprint


@user_blueprint.route("/logout", strict_slashes=False)
def logout():
    """Log profile out"""

    # Forget any user_id
    session.pop("user_id")

    # Redirect profile to log in form
    # flash("Logged out!")
    return redirect("/")
