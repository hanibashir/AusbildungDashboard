from datetime import datetime
from pathlib import Path
from flask import session
from werkzeug.utils import secure_filename
import os


class ImageService:
    def __init__(self, image_db_path=None):
        if image_db_path:
            self.image_db_path = image_db_path
        self.app_folder: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # path/to/app_folder

    def upload_image(self, folder_path, image):
        """ upload image to images folder and return the path to it """
        # add date and user ID to the image name to make it unique dt_obj = datetime.strptime('20.12.2016 09:38:42,
        # 76', '%d.%m.%Y %H:%M:%S,%f') millisec = dt_obj.timestamp() * 1000
        time_in_milli = datetime.now().timestamp() * 1000
        old_name, image_ext = os.path.splitext(image.filename)
        image_name = str(int(time_in_milli)) + "-" + str(session['user_id']) + image_ext
        # get full path to the image
        image_url = os.path.join(self.app_folder, folder_path, secure_filename(image_name))
        # save it in the upload server
        image.save(image_url)
        # get image url without root folder path
        return os.path.join(folder_path + "/" + secure_filename(image_name))  # e.g. /static/images/users/filename.jpg

    def delete_image(self, default_image_path):
        """ delete image"""
        # check if it's the default image
        if self.image_db_path and self.image_db_path != default_image_path:
            # if isn't the default image, try to remove it from images/posts folder
            image_path = os.path.join(self.app_folder, self.image_db_path)
            # delete post image if exist
            if Path(image_path).is_file():
                os.remove(image_path)
