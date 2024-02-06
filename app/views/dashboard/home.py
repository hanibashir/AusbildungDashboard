from flask import render_template
from . import dashboard_blueprint
from ...utils.helpers import login_required


@dashboard_blueprint.route("/dashboard", strict_slashes=False, methods=["GET", "POST"])
@login_required
def dashboard():
    """Show main dashboard"""
    return render_template("dashboard/index.html")
