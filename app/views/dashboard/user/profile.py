import os
from pathlib import Path

from flask import render_template, session, request, flash, redirect, url_for, current_app
from werkzeug.security import check_password_hash

from app.utils.validation.user.user_validator import UserValidator
from . import user_blueprint
from app.utils.helpers import login_required, upload_image
from app.utils.db_queries.user.user_queries import UserQueries


@user_blueprint.route("/user/profile", strict_slashes=False, methods=["GET", "POST"])
@login_required
def profile():
    """User profile"""
    if request.method == "POST":
        """ 
            Receive and validate profile registration data
            # {'name': 'test', 'email': 'test@test.com', 'old_password': 'aA123456',
            # 'password': 'bB123456', 'confirm_password': 'bB123456', 'about': 'about me',
            # 'old_img_url': 'static/images/users/1704295188176_photo-SL5.png' } 
            # old_img_url to delete it from the user images folder if the user changed their photo
        """
        data = request.form.to_dict()  # flat=True
        # return jsonify(data)
        validator = UserValidator(data=data, profile=True)
        queries = UserQueries(data=data)
        validated, validate_msg = validator.validate_profile_update_input()
        if not validated:
            flash(validate_msg)
            # return render_template("auth/register.html")
            return redirect(url_for("user.profile"))

        user = queries.select_user(user_id=session.get("user_id"))
        if not check_password_hash(user.Password, data['old_password']):
            flash("Wrong old password")
            return redirect(url_for("user.profile"))
        # return jsonify(data)
        image = request.files["img"]
        if not image:
            image_short_url = data['old_img_url']
        else:
            # upload and get image path
            image_short_url = upload_image(folder_path=current_app.config["USERS_UPLOAD_FOLDER"], image=image)
            # delete the old image from the folder after uploading the new one
            head, image_name = os.path.split(data['old_img_url'])
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            image_path = os.path.join(project_root, 'static', 'images', 'users', image_name)
            if Path(image_path).is_file():
                os.remove(image_path)

        msg = queries.update_user(user, img_url=image_short_url)
        flash(msg)
        return redirect(url_for("user.profile"))
    else:
        user_id = session.get("user_id")
        queries = UserQueries()
        # Retrieve a profile by ID
        user = queries.select_user(user_id=user_id)

        return render_template("dashboard/user/profile.html", user=user)
