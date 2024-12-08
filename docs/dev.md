# dev

```sh
python manage.py runserver
```

项目结构
```yml
api/:
  routes/
  lib/:
    database.py
  index.py
alembic/:
  env.py
  script.py.mako
  README
  versions/
```

```sh
docs/
alembic.ini
```

## django-ninja

```sh
pip install django-ninja
# 进入 根应用 (项目目录)
cd api
mkdir nj_api
cd nj_api
touch __init__.py
```

```python name="api/nj_api/__init__.py"
from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
```

```python name="api/urls.py"
from django.contrib import admin
from django.urls import path, include
from .nj_api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    ...
    path("api/", api.urls),
]
```

## db
  
```sh
pip install python-dotenv
pip install psycopg2-binary
```

```py name="api/settings.py"
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
load_dotenv()
# Replace the DATABASES section of your settings.py with this
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
print(f"tmpPostgres: {tmpPostgres}")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.replace('/', ''),
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
    },
}
```

```sh
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## django 内置 app, db

### auth

- db:
  - auth_group
    - id
    - name
    - id_auth_group_permissions_group_id
    - id_auth_user_groups_group_id
  - auth_group_permissions
  - auth_permission
  - auth_user
    - id
    - password
    - last_login
    - username
    - first_name
    - last_name
    - email
    - is_superuser
    - is_staff
    - is_active
    - date_joined
    - id_auth_user_groups_user_id
      - id
      - user_id
      - group_id
    - id_auth_user_user_permissions_user_id
      - id
      - user_id
      - permission_id
  - auth_user_groups
  - auth_user_user_permissions

## users

```sh
pip install django-ninja-extra # 类
pip install django-ninja-jwt # jwt
pip install ninja-schema # http IO schema
```
