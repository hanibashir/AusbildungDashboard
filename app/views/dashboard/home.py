from flask import render_template, request, flash, url_for, redirect, current_app
from . import dashboard_blueprint
from app.utils.dashboard_queries.post.post_queries import PostService
from app.utils.dashboard_queries.category.category_queries import CategoryQueries
from ...utils.helpers import login_required
from ...utils.query_obj_to_dict import row_to_dict
from ...utils.imageservice import ImageService


@dashboard_blueprint.route("/dashboard", strict_slashes=False, methods=["GET", "POST"])
@login_required
def home():
    """Show main dashboard"""
    if request.method == 'POST':
        post_queries = PostService()
        form_data = request.form.to_dict()  # flat=True
        if form_data['delete_post']:
            post_id = form_data['delete_post']
            post_to_delete = row_to_dict(post_queries.get_post_by_id(post_id=post_id))
            # if the post has an image
            if post_to_delete['image_url'] is not None or post_to_delete['image_url'] != "":
                ImageService(image_db_path=post_to_delete['image_url']).delete_image(current_app.config["DEFAULT_POST_IMAGE"])

            deleted, delete_post_msg = post_queries.delete_post(post_id)
            if deleted:
                flash(delete_post_msg, 'success')
            else:
                flash(delete_post_msg, 'failed')
            return redirect(url_for('dashboard.home'))
    else:
        post_rows = PostService().get_all_posts()
        posts = [row.to_dict() for row in post_rows]
        cats_rows = CategoryQueries().select_all()
        cats = [row.to_dict() for row in cats_rows]
        return render_template("dashboard/index.html", posts=posts, cats=cats)
