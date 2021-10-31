import os
import re


def get_channeli_oauth_redirect_url(type="Web"):
    """
    Returns the URL to redirect the user to for the channeli OAuth2 flow.
    """

    if type == "mobile":
        return os.getenv("CHANNELI_MOBILE_REDIRECT_URL")
    else:
        return os.getenv("CHANNELI_REDIRECT_URL")
