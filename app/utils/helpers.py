from flask import redirect, session, url_for
from functools import wraps



def login_required(f):
    """ Decorate routes to require login. """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("user.login"))
        return f(*args, **kwargs)
    return decorated_function



