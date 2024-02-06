import os
from pathlib import Path
from flask import flash, redirect, current_app, request, url_for, jsonify
from app.utils.constants import BAD_REQUEST
from app.utils.dashboard_queries.post.post_queries import PostService
from app.utils.helpers import upload_image
from app.utils.validation.post.post_validator import PostValidator


def validate_insert_or_update(command, data):
    queries = PostService(data=data)

    validated, validate_msg = PostValidator(data=data).validate_post_input()

    if not validated:
        flash(validate_msg)
        if command == 'insert':
            return redirect(url_for("dashboard.create_post"))
        elif command == 'update':
            return redirect(url_for("dashboard.edit_post"))

    image = request.files["img"]

    image_short_url = ""

    if not image:
        if command == 'insert':
            image_short_url = os.path.join(current_app.config["IMAGES_UPLOAD_FOLDER"] + "/" + "no_image.jpg")
        elif command == 'update':
            image_short_url = data['old_img_url']
    else:  # there's image
        if command == 'insert':
            # upload and get image path
            image_short_url = upload_image(folder_path=current_app.config["POSTS_UPLOAD_FOLDER"], image=image)
        elif command == 'update':
            # upload and get image path
            image_short_url = upload_image(folder_path=current_app.config["POSTS_UPLOAD_FOLDER"], image=image)
            # delete the old image from the folder after uploading the new one
            head, image_name = os.path.split(data['old_img_url'])
            project_root: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            image_path = os.path.join(project_root, 'static', 'images', 'posts', image_name)
            if Path(image_path).is_file():
                os.remove(image_path)

    if command == 'insert':
        insert_msg = queries.insert_post(image_url=image_short_url)
        flash(insert_msg)
        return redirect(url_for('dashboard.home'))
    elif command == 'update':
        update_msg = (PostService(data=data)
                      .update_post(PostService().
                                   get_post_by_id(data['post_id']), image_url=image_short_url))
        flash(update_msg)
        return redirect(url_for('dashboard.home'))

    flash(BAD_REQUEST)
    return redirect(url_for('dashboard.home'))


