from app.views.dashboard.user import user_blueprint
import os
from flask import url_for, redirect, render_template, request, current_app, flash
from app.services.validation.user.user_validator import UserValidator
from app.data.dashboard_queries.user.user_queries import UserQueries
from app.services.image_service import ImageService


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
        image_service = ImageService()

        validated, validate_msg = validator.validate_registration_input()

        if not validated:
            flash(validate_msg)
            # return render_template("auth/register.html")
            return redirect(url_for("user.register"))
            # return make_response(message_to_json(validate_msg, BAD_REQUEST), BAD_REQUEST)

        # Check if the email already exists in the database
        email_exists, check_email_msg = queries.check_email_exists()
        if email_exists:
            flash("Email exists")
            return redirect("/register")

        # get the image from the form field
        image = request.files["img"]

        if not image:
            image_short_url = os.path.join(
                current_app.config["IMAGES_UPLOAD_FOLDER"] + "/" + current_app.config["DEFAULT_USER_IMAGE"])
        else:
            # get image path
            image_short_url = image_service.upload_image(folder_path=current_app.config["USERS_UPLOAD_FOLDER"], image=image)

        # insert new profile
        insert_msg = queries.insert_user(image_url=image_short_url)
        flash(insert_msg)
        return redirect("/login")
    else:
        return render_template("auth/register.html")
