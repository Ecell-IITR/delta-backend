from uuid import uuid4

def get_profile_image_path(instance, filename):
  return 'PROFILE_IMAGE/user_%s_%s' % (instance.username, filename)


def get_website_logo_image_path(instance, filename):
  return 'WEBSITE_LOGO_IMAGE/website_%s_%s' % (instance.id, filename)

def get_ckeditor_filename(filename):
    ext = filename.split('.')[-1:][0]
    new_filename = uuid4().hex + '.' + ext
    return '/'.join(new_filename)