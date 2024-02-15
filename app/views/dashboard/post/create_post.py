from flask import request, render_template
from app.data.dashboard_queries.category.category_queries import CategoryQueries
from app.data.dashboard_queries.post.validate_insert_or_update import validate_insert_or_update
from app.utils.helpers import login_required
from .. import dashboard_blueprint


@dashboard_blueprint.route("/dashboard/post/create", strict_slashes=False, methods=["GET", "POST"])
@login_required
def create_post():
    """Add new post"""
    if request.method == "POST":
        return validate_insert_or_update(command='insert', data=request.form.to_dict())  # flat=True
    else:
        rows = CategoryQueries().select_all()
        cats_list = [row.to_dict() for row in rows]
        return render_template("dashboard/post/create_post.html", cats=cats_list)
