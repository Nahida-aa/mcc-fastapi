# Alembic

## commmands

### 1. 初始化 Alembic

```sh
alembic init alembic
```

### 2. 查看当前数据库版本

```sh
alembic current
```

### 3. 创建迁移脚本

```sh
alembic revision --autogenerate -m "1"
```

#### err

##### Target database is not up to date 目标数据库不是最新的

```sh
alembic stamp head
```

### 4. 应用迁移(升级数据库到最新版本)

```sh
alembic upgrade head
```

#### 迁移 err

##### DuplicateColumn 重复列

需要手动删除重复列:

```sql
ALTER TABLE "user" DROP COLUMN IF EXISTS avatar;
```

##### DependentObjectsStillExist 依赖对象仍然存在

手动删除依赖的外键约束:

```sql
ALTER TABLE useridentitylink DROP CONSTRAINT IF EXISTS useridentitylink_user_id_fkey;
```

```sh
# 回滚到上一个版本
alembic downgrade -1
# 回滚到初始版本
alembic downgrade base
# 回滚到指定版本
alembic downgrade <revision>
```

不能删表，现在生产数据库是旧结构，本地的代码是新的 ？


在这种情况下，你需要确保生产数据库与 Alembic 的迁移记录同步。以下是解决这个问题的步骤：

1. **手动同步 Alembic 迁移记录**：将生产数据库标记为最新版本。
2. **生成新的迁移脚本**：根据新的模型生成迁移脚本。
3. **应用迁移**：将新的迁移应用到生产数据库。

### 1. 手动同步 Alembic 迁移记录

首先，将生产数据库标记为最新版本。使用以下命令将数据库标记为最新版本：

```sh
alembic stamp head
```

### 2. 生成新的迁移脚本

确保数据库状态与 Alembic 的迁移记录一致后，生成新的迁移脚本：

```sh
alembic revision --autogenerate -m "Add age field to User model"
```

### 3. 应用迁移

运行以下命令来应用迁移：

```sh
alembic upgrade head
```