def get_profile_image_path(instance, filename):
  return f'PROFILE_IMAGE/user_{instance.username}_{filename}'


def get_website_logo_image_path(instance, filename):
  return f'WEBSITE_LOGO_IMAGE/website_{instance.id}_{filename}'