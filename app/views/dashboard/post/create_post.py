from flask import request, flash, url_for, redirect, render_template, current_app
from app.utils.db.post_queries import PostQueries
from app.utils.db.category_queries import CategoryQueries
from app.utils.helpers import login_required
from app.utils.validation.post_validator import PostValidator
from app.utils.helpers import upload_image
from .. import dashboard_blueprint


@dashboard_blueprint.route("/dashboard/post/create", methods=["GET", "POST"])
@login_required
def create_post():
    """Add new posts"""
    if request.method == "POST":
        """
            {
                'title': 'test title',
                'duration': '3 years',
                'content': 'test content',
                'certificate': 'secondary school',
                'first_year_salary ': '700',
                'second_year_salary ': '800',
                'third_year_salary ': '900',
                'fourth_year_salary ': '1100',
                'shift_type': 'full time',
                'category_id': '1',
                'best_paid': '1', # or '0'
                'popular': '1', # or '0'
                'publish': '1' # or '0'
            }
        """
        data = request.form.to_dict()  # flat=True
        validator = PostValidator(data=data)
        queries = PostQueries(data=data)

        validated, validate_msg = validator.validate_post_input()

        if not validated:
            flash(validate_msg)
            return redirect(url_for("dashboard.create_post"))

        image = request.files["img"]
        # get image path
        image_short_path = upload_image(folder_path=current_app.config["POSTS_UPLOAD_FOLDER"], image=image)

        insert_msg = queries.insert_post(image_short_path=image_short_path)
        flash(insert_msg)
        return redirect("/dashboard")

    else:
        rows = CategoryQueries().select_all()
        cats_list = [row.to_dict() for row in rows]
        return render_template("dashboard/posts/create_post.html", cats=cats_list)
