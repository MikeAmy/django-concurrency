import django
from django.utils import timezone
import pytest
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django_webtest import WebTestMixin
from tests.admin import admin_register_models

SENTINEL = '**concurrent_update**'

from concurrency.api import apply_concurrency_check
from django.contrib.auth.models import Permission
from concurrency.fields import IntegerVersionField

apply_concurrency_check(Permission, 'version', IntegerVersionField)

DJANGO_TRUNK = django.VERSION[:2] >= (1, 8)

win32only = pytest.mark.skipif("sys.platform != 'win32'")

skipIfDjangoVersion = lambda v: pytest.mark.skipif(django.VERSION[:2] >= v,
                                                   reason="Skip if django>={}".format(v))


class AdminTestCase(WebTestMixin, TransactionTestCase):
    urls = 'tests.urls'

    def setUp(self):
        super(AdminTestCase, self).setUp()

        self.user, __ = User.objects.get_or_create(is_superuser=True,
                                                   is_staff=True,
                                                   is_active=True,
                                                   last_login=timezone.now(),
                                                   email='sax@example.com',
                                                   username='sax')
        admin_register_models()


# class DjangoAdminTestCase(TransactionTestCase):
#     urls = 'concurrency.tests.urls'
#     MIDDLEWARE_CLASSES = global_settings.MIDDLEWARE_CLASSES
#     AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS
#
#     def setUp(self):
#         super(DjangoAdminTestCase, self).setUp()
#         self.sett = self.settings(
#             #INSTALLED_APPS=INSTALLED_APPS,
#             MIDDLEWARE_CLASSES=self.MIDDLEWARE_CLASSES,
#             AUTHENTICATION_BACKENDS=self.AUTHENTICATION_BACKENDS,
#             PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),  # fastest hasher
#             STATIC_URL='/static/',
#             SOUTH_TESTS_MIGRATE=False,
#             TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'templates'),))
#         self.sett.enable()
#         django.core.management._commands = None  # reset commands cache
#         django.core.management.call_command('syncdb', verbosity=0)
#
#         # admin_register(TestModel0)
#         # admin_register(TestModel1, TestModel1Admin)
#
#         self.user, __ = User.objects.get_or_create(username='sax',
#                                                    is_active=True,
#                                                    is_staff=True,
#                                                    is_superuser=True)
#         self.user.set_password('123')
#         self.user.save()
#         self.client.login(username=self.user.username, password='123')
#         # self.target, __ = TestModel0.objects.get_or_create(username='aaa')
#         # self.target1, __ = TestModel1.objects.get_or_create(username='bbb')
#
#     def tearDown(self):
#         super(DjangoAdminTestCase, self).tearDown()
#         self.sett.disable()
#         # admin_unregister(TestModel0, TestModel1)
