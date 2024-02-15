from flask import render_template, request, flash, url_for, redirect, current_app
from . import dashboard_blueprint
from app.data.dashboard_queries.post.post_queries import PostQueries
from app.data.dashboard_queries.category.category_queries import CategoryQueries
from ...utils.helpers import login_required
from ...services.post.post_service import PostService


@dashboard_blueprint.route("/dashboard", strict_slashes=False, methods=["GET", "POST"])
@login_required
def home():
    """Show main dashboard"""
    if request.method == 'POST':
        form_data = request.form.to_dict()  # flat=True
        if form_data['delete_post']:
            deleted, delete_post_msg = PostService(form_data['delete_post']).delete_post()
            if deleted:
                flash(delete_post_msg, 'success')
            else:
                flash(delete_post_msg, 'failed')
        return redirect(url_for('dashboard.home'))
    else:
        post_rows = PostQueries().get_all_posts()
        posts = [row.to_dict() for row in post_rows]
        cats_rows = CategoryQueries().select_all()
        cats = [row.to_dict() for row in cats_rows]
        return render_template("dashboard/index.html", posts=posts, cats=cats)
