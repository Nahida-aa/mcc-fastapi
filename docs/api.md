这些 API 端点主要用于用户管理和认证，包括创建用户、启用/禁用用户、删除用户、用户登录和刷新令牌。你可以使用 Django Ninja 提供的自动生成 API 文档功能来生成 API 文档，供前端开发人员参考。

### API 端点说明

1. **创建用户**：
   - **URL**：`/auth/create`
   - **方法**：`POST`
   - **请求体**：`CreateUserSchema`
   - **响应**：`UserTokenOutSchema`

2. **启用/禁用用户**：
   - **URL**：`/auth/{pk}/enable-disable`
   - **方法**：`PUT`
   - **请求参数**：`pk`（用户 ID）
   - **响应**：`EnableDisableUserOutSchema`

3. **删除用户**：
   - **URL**：`/auth/{pk}/delete`
   - **方法**：`DELETE`
   - **请求参数**：`pk`（用户 ID）
   - **响应**：`EnableDisableUserOutSchema`

4. **用户登录**：
   - **URL**：`/auth/login`
   - **方法**：`POST`
   - **请求体**：`TokenObtainSlidingSerializer`
   - **响应**：`UserTokenOutSchema`

5. **刷新令牌**：
   - **URL**：`/auth/api-token-refresh`
   - **方法**：`POST`
   - **请求体**：`TokenRefreshSlidingSchema`
   - **响应**：`TokenRefreshSlidingSerializer`

### 编写 API 文档

你可以使用 Django Ninja 提供的自动生成 API 文档功能来生成 API 文档。以下是如何编写 API 文档的示例：

#### 1. 定义 API 端点

在 

api.py

 中定义 API 端点：

```python
from .models import User
from ninja_extra import NinjaExtraAPI, api_controller, route, status
from ninja_extra.permissions import IsAdminUser, IsAuthenticated
from ninja_jwt import schema
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import TokenObtainSlidingController
from ninja_jwt.tokens import SlidingToken
from datetime import datetime
from users.schema import (
    CreateUserSchema,
    EnableDisableUserOutSchema,
    EnableDisableUserSchema,
    UserTokenOutSchema,
)

api = NinjaExtraAPI()

@api_controller("/auth", tags=["users"], auth=JWTAuth())
class UserController:
    @route.post(
        "/create", response={201: UserTokenOutSchema}, url_name="user-create", auth=None
    )
    def create_user(self, user_schema: CreateUserSchema):
        user = user_schema.create()
        token = SlidingToken.for_user(user)
        return UserTokenOutSchema(
            user=user,
            token=str(token),
            token_exp_date=datetime.utcfromtimestamp(token["exp"]),
        )

    @route.put(
        "/{int:pk}/enable-disable",
        permissions=[IsAuthenticated, IsAdminUser],
        response=EnableDisableUserOutSchema,
        url_name="user-enable-disable",
    )
    def enable_disable_user(self, pk: int):
        user_schema = EnableDisableUserSchema(user_id=str(pk))
        user_schema.update()
        return EnableDisableUserOutSchema(message="Action Successful")

    @route.delete(
        "/{int:pk}/delete",
        permissions=[IsAuthenticated, IsAdminUser],
        response=EnableDisableUserOutSchema,
        url_name="user-delete",
    )
    def delete_user(self, pk: int):
        user_schema = EnableDisableUserSchema(user_id=str(pk))
        user_schema.delete()
        return self.create_response("", status_code=status.HTTP_204_NO_CONTENT)


@api_controller("/auth", tags=["auth"])
class UserTokenController(TokenObtainSlidingController):
    auto_import = True

    @route.post("/login", response=UserTokenOutSchema, url_name="login")
    def obtain_token(self, user_token: schema.TokenObtainSlidingSerializer):
        user = user_token._user
        token = SlidingToken.for_user(user)
        return UserTokenOutSchema(
            user=user,
            token=str(token),
            token_exp_date=datetime.utcfromtimestamp(token["exp"]),
        )

    @route.post(
        "/api-token-refresh",
        response=schema.TokenRefreshSlidingSerializer,
        url_name="refresh",
    )
    def refresh_token(self, refresh_token: schema.TokenRefreshSlidingSchema):
        refresh = schema.TokenRefreshSlidingSerializer(**refresh_token.dict())
        return refresh

api.add_controller(UserController)
api.add_controller(UserTokenController)
```

#### 2. 配置 URL 路由

在 `urls.py` 中包含 API 路由：

```python
from django.contrib import admin
from django.urls import path
from api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
```

#### 3. 生成 API 文档

Django Ninja 提供了自动生成 API 文档的功能。你可以通过访问 `/api/docs` 路径查看自动生成的 API 文档。

### 示例 API 文档

访问 `http://127.0.0.1:8000/api/docs` 可以查看自动生成的 API 文档。以下是示例 API 文档的内容：

#### 创建用户

- **URL**：`/auth/create`
- **方法**：`POST`
- **请求体**：

```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "username": "string",
  "is_staff": true,
  "is_superuser": true,
  "password": "string"
}
```

- **响应**：

```json
{
  "user": {
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "username": "string",
    "id": 0,
    "is_active": true
  },
  "token": "string",
  "token_exp_date": "2023-10-10T10:10:10Z"
}
```

#### 启用/禁用用户

- **URL**：`/auth/{pk}/enable-disable`
- **方法**：`PUT`
- **请求参数**：`pk`（用户 ID）
- **响应**：

```json
{
  "message": "Action Successful"
}
```

#### 删除用户

- **URL**：`/auth/{pk}/delete`
- **方法**：`DELETE`
- **请求参数**：`pk`（用户 ID）
- **响应**：

```json
{
  "message": "Action Successful"
}
```

#### 用户登录

- **URL**：`/auth/login`
- **方法**：`POST`
- **请求体**：

```json
{
  "username": "string",
  "password": "string"
}
```

- **响应**：

```json
{
  "user": {
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "username": "string",


   

 "id": 0,
    "is_active": true
  },
  "token": "string",
  "token_exp_date": "2023-10-10T10:10:10Z"
}
```

#### 刷新令牌

- **URL**：`/auth/api-token-refresh`
- **方法**：`POST`
- **请求体**：

```json
{
  "refresh": "string"
}
```

- **响应**：

```json
{
  "token": "string"
}
```

### 结论

通过使用 Django Ninja 提供的自动生成 API 文档功能，你可以轻松生成 API 文档，供前端开发人员参考。API 文档包括每个端点的 URL、方法、请求体和响应示例。访问 `http://127.0.0.1:8000/api/docs` 可以查看自动生成的 API 文档。

找到具有 1 个许可证类型的类似代码