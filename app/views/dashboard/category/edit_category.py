from flask import request, render_template
from .. import dashboard_blueprint
from app.database.dashboard_queries.category.category_queries import CategoryQueries
from app.utils.helpers import login_required
from app.utils.query_obj_to_dict import row_to_dict


@dashboard_blueprint.route("/dashboard/category", strict_slashes=False, methods=["GET", "POST"])
@login_required
def edit_category():
    if request.method == "POST":
        pass
    else:
        action = request.args.get("action")
        if action:
            if action == "edit":
                category_id = request.args.get("category_id")
                category = row_to_dict(CategoryQueries().select_category(category_id=category_id))
                return render_template("dashboard/category/edit_category.html", category=category)
