from app.views.dashboard.user import user_blueprint
import os
from flask import url_for, redirect, render_template, request, current_app, flash
from ...utils.validation.user_validator import UserValidator
from ...utils.db.user_queries import UserQueries
from ...utils.helpers import upload_image


# register profile
@user_blueprint.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register():
    """Register new profile"""
    # User reached route via POST
    if request.method == "POST":
        # Receive and validate profile registration data
        # {'name': 'test', 'email': 'test@test.com', 'password': '12345678', 'confirm_password': '12345678'}
        data = request.form.to_dict()  # flat=True

        validator = UserValidator(data=data)
        queries = UserQueries(data=data)

        validated, validate_msg = validator.validate_user_input()

        if not validated:
            flash(validate_msg)
            return render_template("auth/register.html")
            # return redirect(url_for("auth.register"))
            # return make_response(message_to_json(validate_msg, BAD_REQUEST), BAD_REQUEST)

        # Check if the email already exists in the database
        email_exists, check_email_msg = queries.check_email_exists()
        if email_exists:
            flash("Email exists")
            return redirect(url_for("auth.register"))

        # get the image from the form field
        image = request.files["img"]

        if not image:
            image_short_url = os.path.join(current_app.config["IMAGES_UPLOAD_FOLDER"] + "/" +
                                           "profile-blue-thumbnail.png")
        else:
            # get image path
            image_short_url = upload_image(folder_path=current_app.config["USERS_UPLOAD_FOLDER"], image=image)

        # insert new profile
        insert_msg = queries.insert_user(image_short_url)
        flash(insert_msg)
        return redirect("/login")
    else:
        return render_template("auth/register.html")
