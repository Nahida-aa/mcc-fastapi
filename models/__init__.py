# 简化导入路径：其他模块只需要导入 models 包，而不需要分别导入各个模型，简化了导入路径
# 避免循环导入：某些情况下，集中导入可以帮助避免循环导入问题
# 集中管理：方便进行模型的集中管理和维护，可以在一个地方查看和修改所有模型的导入
from .user_model import User, UserPublic, UserPlatformInfo
from .team_model import Team
from api.models.identity_model import Identity
from api.models.tag_model import Tag
from api.models.proj_model import Proj
from api.models.resource_model import Resource
# from .group_model import Group
# from .role_model import Role
# from .hero_model import Hero
# from .media_model import Media
# from .image_media_model import ImageMedia
# from .user_follow_model import UserFollow