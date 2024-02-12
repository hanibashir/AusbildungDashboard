from flask import request, redirect, url_for, flash, render_template
from ....services.category.category_service import CategoryService
from .. import dashboard_blueprint
from app.utils.helpers import login_required


@dashboard_blueprint.route("/dashboard/category/create", strict_slashes=False, methods=["GET", "POST"])
@login_required
def create_category():
    """Add new category"""
    if request.method == "POST":
        data = request.form.to_dict()  # flat=True
        inserted, insert_msg = CategoryService(data).insert_category()
        if not inserted:
            flash(insert_msg)
            return redirect(url_for('dashboard.create_category'))
        flash(insert_msg)
        return redirect(url_for('dashboard.home'))
    else:
        return render_template("dashboard/category/create_category.html")
