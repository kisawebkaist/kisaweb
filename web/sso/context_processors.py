import yaml

import os
from .models import LoginError
from web.settings import BASE_DIR

def login_error(request):
    if LoginError.objects.all().exists():
        login_error_object = LoginError.objects.all()[0]
    else:
        with open(os.path.join(BASE_DIR, 'data/required.yaml')) as f:
            parsed = yaml.safe_load(f)
            fields = next((d for d in parsed if d['model']=='sso.models.LoginError'))['fields']
            login_error_object = LoginError.objects.create(**fields)
    return {'login_error': login_error_object}