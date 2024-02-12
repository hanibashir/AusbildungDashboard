from flask import request, url_for, redirect, render_template
from app.database.dashboard_queries.category.category_queries import CategoryQueries
from app.database.dashboard_queries.post.post_queries import PostQueries
from app.database.dashboard_queries.post.validate_insert_or_update import validate_insert_or_update
from app.utils.query_obj_to_dict import row_to_dict, rows_to_dict
from app.utils.helpers import login_required
from .. import dashboard_blueprint


@dashboard_blueprint.route("/dashboard/post", strict_slashes=False, methods=["GET", "POST"])
@login_required
def edit_post():
    """Update post"""
    if request.method == "POST":
        return validate_insert_or_update(command='update', data=request.form.to_dict())  # flat=True
    else:
        action = request.args.get("action")
        if action:
            if action == "edit":
                post_id = request.args.get("post_id")
                post = row_to_dict(PostQueries().get_post_by_id(post_id=post_id))
                post_cat = row_to_dict(CategoryQueries().select_category(category_id=post['category_id']))
                categories = rows_to_dict(CategoryQueries().select_all())
                return render_template(
                    "dashboard/post/edit_post.html",
                    post=post,
                    post_cat=post_cat,
                    category=categories
                )
        else:
            return redirect(url_for('dashboard.home'))
