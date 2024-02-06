import datetime
from flask import redirect, session, url_for
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import os


def login_required(f):
    """ Decorate routes to require login. """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("profile.login"))
        return f(*args, **kwargs)

    return decorated_function


def upload_image(folder_path, image):
    """ upload image to images folder and return the path to it """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # add date to image name to make it unique
    # dt_obj = datetime.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f') millisec = dt_obj.timestamp() * 1000
    time_in_milli = datetime.now().timestamp() * 1000
    image_name = str(int(time_in_milli)) + " " + image.filename
    # get full path to the image
    image_url = os.path.join(project_root, folder_path, secure_filename(image_name))
    # save it in the upload server
    image.save(image_url)
    # get image url without root folder path
    return os.path.join(folder_path + "/" + secure_filename(image_name))  # e.g. /static/images/users/filename.jpg
