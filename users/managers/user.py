from django.contrib.auth import models as auth_models


class UserManager(auth_models.BaseUserManager):
    """
    This is the manager for objects of class AuthUser
    """

    def _create_instance(self, username, email, password, is_admin):
        """
        Create a user with the given password
        Both standard and administrative users are identical at this level
        :param username: the username for the user
        :param password: the password for the user
        :return: the newly created user
        """

        if not password:
            raise ValueError('Password is required')
        user = self.model(
            username=username,
            email=email,
            is_admin=is_admin,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username='', email='', password=None):
        """
        Create a standard user with the given password
        :param username: the username for the standard user
        :param password: the password for the standard user
        :return: the newly created standard user
        """

        return self._create_instance(
            username=username,
            email=email,
            password=password,
            is_admin=False
        )

    def create_superuser(self, username='', email='', password=None):
        """
        Create an administrative user with the given password
        :param username: the username that will be ignored
        :param password: the password for the administrative user
        :return: the newly created administrative user
        """

        return self._create_instance(
            username=username,
            email=email,
            password=password,
            is_admin=True
        )
