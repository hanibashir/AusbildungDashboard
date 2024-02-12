from app.database.dashboard_queries.post.post_queries import PostQueries
from app.services.image_service import ImageService
from app.utils.query_obj_to_dict import row_to_dict
from flask import current_app, flash


class PostService:
    def __init__(self, post_id):
        self.post_id = post_id

    def delete_post(self):
        post_queries = PostQueries()
        post_to_delete = row_to_dict(post_queries.get_post_by_id(post_id=self.post_id))
        # if the post has an image
        if post_to_delete['image_url'] is not None or post_to_delete['image_url'] != "":
            ImageService(
                image_db_path=post_to_delete['image_url']
            ).delete_image(
                current_app.config["DEFAULT_POST_IMAGE"]
            )

        deleted, delete_post_msg = post_queries.delete_post(self.post_id)
        return deleted, delete_post_msg
