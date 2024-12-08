# structure

## 超集

### User

```ts
type User = {
  id: int
  created: Date
  updated: Date
  "last_login": "string", // 最后登录时间
  "username": "string",
  "password": "string",
  "email": "string",
  "nickname": "string",
  "is_superuser": "boolean", // 是否是超级用户
  "is_staff": "boolean", // 是否是员工
  "is_active": "boolean", // 是否激活
  "role": "string",
  "avatar_url": "string",
  "phone": "string", // 手机号
  "id_card": "string", // 身份证号
  // 平台身份 对象列表 : 创作者, 投资者, 施工者, 鉴赏者, ...
  "identities": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "created": "string",
      "updated": "string",
      "status": "string",
      "avatar_url": "string",
      "description": "string"
    }
  ],
  // 加入的团队
  "teams": [
    {
      "id": "string",
      "username": "string",
      "role": "string",
      "created": "string",
      "updated": "string",
      "status": "string",
      "avatar_url": "string",
      "description": "string",
      "members": [
        {
          "id": "string",
          "username": "string",
          "role": "string",
          "avatar_url": "string",
          "description": "string"
        }
      ]
    }
  ],
}
```

### Permission
  
```ts

```
