import functools
from flask import g, redirect, url_for, abort

def login_required(func):
    """
    Checks if the current user is logged in and redirects her to the login
    page if not.
    """
    @functools.wraps(func)
    def _func(*args, **kwargs):
        if not hasattr(g, 'user'):
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)
    return _func

def admin_required(func):
    """
    Checks if the current user is an administrator and redirects her
    to the login page if not.
    """
    @functools.wraps(func)
    def _func(*args, **kwargs):
        if not hasattr(g, 'user'):
            return redirect(url_for('login', next=request.path))
        if g.user.roles is None or not 'admin' in g.user.roles:
            return abort(403)
        return func(*args, **kwargs)
    return _func
