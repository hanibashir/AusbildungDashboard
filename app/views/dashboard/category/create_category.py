import os

from flask import request, redirect, url_for, flash, render_template, current_app
from .. import dashboard_blueprint
from app.utils.dashboard_queries.category.category_queries import CategoryQueries
from app.utils.helpers import login_required
from app.utils.imageservice import ImageService
from app.utils.validation.category.category_validator import CategoryValidator


@dashboard_blueprint.route("/dashboard/category/create", strict_slashes=False, methods=["GET", "POST"])
@login_required
def create_category():
    """Add new category"""
    if request.method == "POST":
        """
            {
                'title': 'cat title',
                'description': 'cat description',
                'image_url': '/static/images/category/cat.png'
            }
        """
        data = request.form.to_dict()  # flat=True
        validator = CategoryValidator(data=data)
        queries = CategoryQueries(data=data)
        image_service = ImageService()

        validated, validate_msg = validator.validate_category_input()

        if not validated:
            flash(validate_msg)
            return redirect(url_for("dashboard.create_category"))

        # Query database to check if category already exists
        if CategoryQueries().select_category(title=data['title']):
            flash("Category already exists")
            return redirect(url_for('dashboard.create_category'))

        image = request.files["img"]
        if not image:
            image_short_url = os.path.join(
                current_app.config["IMAGES_UPLOAD_FOLDER"] + "/" + "no_image.jpg")
        else:
            # get image path
            image_short_url = image_service.upload_image(folder_path=current_app.config["CATS_UPLOAD_FOLDER"], image=image)

        # insert into category table
        insert_msg = queries.insert_category(image_url=image_short_url)
        flash(insert_msg)
        return redirect("/dashboard")
    else:
        return render_template("dashboard/category/create_category.html")
