from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.hashers import check_password

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    
    first_name    = models.CharField(_('first name'),max_length = 250)
    last_name    = models.CharField(_('last name'),max_length = 250)
    username    = models.CharField(_('user name'),max_length = 250, unique=True)
    email         = models.EmailField(_('email'), unique=True)
    phone         = models.CharField(_('phone'), max_length = 20)
    address       = models.CharField(_('address'), max_length = 250, null = True)
    password      = models.CharField(_('password'), max_length=300)
    is_staff      = models.BooleanField(_('staff'), default=True)
    is_admin      = models.BooleanField(_('admin'), default= False)
    is_active     = models.BooleanField(_('active'), default=True)
    date_joined   = models.DateField(_('date joined'), auto_now_add=True)
    time_joined   = models.TimeField(_('time joined'), auto_now_add=True, null = True)

    
    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email