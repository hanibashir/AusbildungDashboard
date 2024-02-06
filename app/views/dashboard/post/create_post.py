import os

from flask import request, flash, url_for, redirect, render_template, current_app
from app.utils.db_queries.post.post_queries import PostService
from app.utils.db_queries.category.category_queries import CategoryQueries
from app.utils.helpers import login_required
from app.utils.post_utils.validate_insert_or_update import validate_insert_or_update
from app.utils.validation.post.post_validator import PostValidator
from app.utils.helpers import upload_image
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
