from django.conf import settings
if 'SweetPy.geely_auth' in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS.append('SweetPy.geely_auth')
if 'rest_framework' in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS.append('rest_framework')
print('注册用户组件')