from flask import render_template
from . import blog_blueprint


@blog_blueprint.route("/", methods=["GET"])
def index():
    """Show latest blog posts"""
    return render_template("blog/index.html")