type User = {
  id: number
  created: Date
  updated: Date
  last_login: Date, // 最后登录时间
  "username": "string",
  "password": "string",
  "email": "string",
  "nickname": "string",
  "is_superuser": boolean // 是否是超级用户
  "is_staff": "boolean", // 是否是员工
  "is_active": "boolean", // 是否激活
  "role": "string",
  "avatar_url": "string",
  phone: string, // 手机号
  // 联系方式
  contact: string
  id_card: string // 身份证号
  // 是否实名认证
  is_real_name: boolean
  age: number // 年龄
  // 门牌号
  door_number: string
  // 性别:
  gender: string
  platform_info?: JSON | PlatformInfo // 平台信息
  is_identity_verified: boolean // 是否已经身份验证, 否则还是游客
  identities?: Identity[] // 拥有的身份
  is_independent: boolean // 是否独立用户
  willing_to_join_team: boolean // 是否愿意加入团队
  teams: Team[] // 加入的团队
  // 参与的项目, 
  projects: Project[] 
  // 通讯录: User[] 
  contacts: User[]
  // 来访信息: User[]
  visitors: User[]
}
type PlatformInfo = {
  mc_experience?: string // 玩 mc 多久了: 0-1年, 1-3年, 3-5年, 5-8年, 8-12年, 12年以上。默认值为 '0-1年'
  play_reason?: string // 为什么会玩 mc: 可以不填。默认值为空字符串
  server_type?: string // 服务器玩家 | 公益服 | 盈利服 | 多人竞技服 | 多人合作服。默认值为 '服务器玩家'
  favorite_content?: {
    building: boolean // 建筑内容。默认值为 false
    survival: boolean // 生存内容。默认值为 false
    adventure: boolean // 冒险内容。默认值为 false
    technology: boolean // 科技内容。默认值为 false
  }
  desired_partners?: string // 平台内想结识怎样的伙伴: 拒绝社交|服务器伙伴|同好建筑内容的伙伴|同好生存内容的伙伴|同好冒险内容的伙伴|同好科技内容的伙伴。默认值为 '拒绝社交'
}
type Identity = {
  id: number
  created: Date
  updated: Date
  name: string // 身份名称: 创作者, 投资者, 施工者, 鉴赏者, ...
  level: number // 身份评级
  status: string // 身份状态
  motivation: string // 身份动机: 初心
  total_interactions: number // 总互动次数
  reputation: JSON // 声誉信息: 口碑情况
  credit: JSON // 信用信息
  additional_info?: JSON // 额外信息
}
type UserDB = {
  id: number
  created: Date
  updated: Date
  last_login: Date
  username: string
  password: string
  email: string
  nickname: string
  is_superuser: boolean
  is_staff: boolean
  is_active: boolean
  role: string
  avatar_url: string
  phone: string
  id_card: string
  platform_info?: JSON
}
type ReadUserOut = {
  id: number
  created: Date
  updated: Date
  last_login: Date
  username: string
  email: string
  nickname: string
  is_active: boolean
}
type UserBaseInfo = {
  username: string // 账户名: 6-8个中文字符, 不支持英文、数字、符号。 检查是否重复(被占用)
  password: string
  phone: string, // 手机号
  id_card: string, // 身份证号
  avatar_url: string // 用户上传头像: 然后存到某次, 将url存到数据库. 其实我觉得可以不对此必填
}

type CreateUserIn = {
  user: UserBaseInfo
  platform_info?: JSON | PlatformInfo // 平台信息: 
}
type CreateUserOut = {
  user: ReadUserOut
  token: string
  token_exp_date: Date
}

type Team = {
  id: number
  created: Date
  updated: Date
  last_login: Date
  creator: User
  name: string
  description: string
  avatar_url: string
  members: User[]
}
type Project = {
  id: number
  created: Date
  updated: Date
  last_login: Date
  creator: User
  name: string
  description: string
  avatar_url: string
  members: User[] | Team[] // 参与者
  status: string // 项目状态
}

type Permission = {
  id: number
  content_type: ContentType
  name: string // Can view model_name, Can add model_name, Can change model_name, Can delete model_name
  codename: string // view_modelName, add_modelName, change_modelName, delete_modelName
}

type ContentType = {
  id: number
  app_label: string
  model: string
}