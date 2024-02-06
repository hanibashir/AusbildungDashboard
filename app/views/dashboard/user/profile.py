from flask import render_template, session
from . import user_blueprint
from app.utils.helpers import login_required
from app.utils.db.user_queries import UserQueries


@user_blueprint.route("/user/profile", strict_slashes=False, methods=["GET", "POST"])
@login_required
def profile():
    """User profile"""

    user_id = session.get("user_id")
    queries = UserQueries()
    # Retrieve a profile by ID
    user = queries.select_user(user_id=user_id)

    return render_template("../templates/dashboard/user/profile.html", user=user)
