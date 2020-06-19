from uuid import uuid4

def get_profile_image_path(instance, filename):
  return f'PROFILE_IMAGE/user_{instance.username}_{filename}'


def get_website_logo_image_path(instance, filename):
  return f'WEBSITE_LOGO_IMAGE/website_{instance.id}_{filename}'

def get_ckeditor_filename(filename):
    ext = filename.split('.')[-1:][0]
    new_filename = uuid4().hex + '.' + ext
    return '/'.join(new_filename)