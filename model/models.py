# -*- coding: utf-8 -*-
# ------------Oooo---
# -----------(----)---
# ------------)--/----
# ------------(_/-
# ----oooO----
# ----(---)----
# -----\--(--
# ------\_)-
# ----
#     author : Yprisoner
#     email : yyprisoner@gmail.com
#                            ------
#    「 涙の雨が頬をたたくたびに美しく 」
import logging
from extends.utils import gettimestamp, sha1_encrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.util._collections import AbstractKeyedTuple
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey

logger = logging.getLogger(__name__)

Base = declarative_base()

'''
    常用的SQLAlchemy字段类型:
    Integer         int                 普通整数，一般是32位
    SmallInteger    int                 取值范围小的整数，一般是16位
    BigInteger      int或long            不限制精度的整数
    Float           float               浮点数
    Numeric         decimal.Decimal     普通整数，一般是32位
    String          str                 变长字符串
    Text            str                 变长字符串，对较长或不限长度的字符串做了优化
    Unicode         unicode             变长Unicode字符串
    UnicodeText     unicode             变长Unicode字符串，对较长或不限长度的字符串做了优化
    Boolean         bool                布尔值
    Date            datetime.date       时间
    Time            datetime.datetime   日期和时间
    LargeBinary     str                 二进制文件
    
    常用的SQLAlchemy列选项:
    primary_key     如果为True，代表表的主键
    autoincrement   如果为True，自动递增
    unique          如果为True，代表这列不允许出现重复的值
    index           如果为True，为这列创建索引，提高查询效率
    nullable        如果为True，允许有空值，如果为False，不允许有空值
    default         为这列定义默认值
    
    常用的SQLAlchemy关系选项:
    backref         在关系的另一模型中添加反向引用
    relationship    关联两张表
    primaryjoin     明确指定两个模型之间使用的联结条件
    uselist         如果为False，不使用列表，而使用标量值
    order_by        指定关系中记录的排序方式
    secondary       指定多对多中记录的排序方式
    secondaryjoin   在SQLAlchemy中无法自行决定时，指定多对多关系中的二级联结条件
'''

def to_dict(res_obj):
    if not res_obj:
        return None
    if isinstance(res_obj, list):  # 列表解析
        if len(res_obj) == 0:
            return None
        if isinstance(res_obj[0], AbstractKeyedTuple):  #
            return [dict(zip(result.keys(), result)) for result in res_obj]
        elif isinstance(res_obj[0], Base):
            try:
                [item.__dict__.pop("_sa_instance_state") for item in res_obj]
            except Exception as e:
                pass
            return [item.__dict__ for item in res_obj]
        elif isinstance(res_obj[0], dict):
            return res_obj
        else:
            return None
    else:
        return db_data_to_dict(res_obj)


### 数据库返回单个数据 转 dict
def db_data_to_dict(res_obj):
    if not res_obj:
        return None
    if isinstance(res_obj, dict):
        return res_obj
    elif isinstance(res_obj, AbstractKeyedTuple):
        return dict(zip(res_obj.keys(), res_obj))
    elif isinstance(res_obj, Base):
        try:
            res_obj.__dict__.pop("_sa_instance_state")
        except Exception as e:
            pass
        return res_obj.__dict__
    else:
        return None

### 用户表
class Users(Base):
    __tablename__ = 'mex_user'

    # ID 主键 自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 邮箱 唯一 不为空
    user_email = Column(String(128), unique=True, nullable=False)
    # 密码 不为空
    user_pass = Column(String(256), nullable=False)
    # 昵称
    user_nickname = Column(String(32))
    # 头像
    user_avatar = Column(String(128))
    # 主页
    user_url = Column(String(128))
    # 一句话简介
    user_introduction = Column(String(512))
    # 注册时间
    user_register_at = Column(Integer, default=gettimestamp())
    # 账号状态
    user_status = Column(String(16), nullable=False, default='normal')
    # 用户分类(权限)
    user_group = Column(String(16), nullable=False, default='user')

    __mapper_args__ = {
        "order_by": id.desc()
    }

    def verify_password(self, password):
        return self.user_pass == sha1_encrypt(password)

    def reset_password(self, password):
        self.user_pass = sha1_encrypt(password)

### 分类 标签
class Attributes(Base):
    __tablename__ = 'mex_attribute'

    # ID 主键 自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 名称 唯一 不能为空
    name = Column(String(64), unique=True, nullable=False)
    # 简写 用于 url 访问 唯一
    slug = Column(String(128), unique=True)
    # 类型  类别 / Tag
    type = Column(String(16), default="category")
    # 简介
    description = Column(Text)
    # 描述图像
    poster = Column(String(256))
    # 标签风格
    style = Column(String(16), default='')
    # 关联Posts表
    posts = relationship('Posts', backref='mex_attribute', lazy="dynamic")

    def __repr__(self):
        return '<Attribute %r>' % self.name

### 内容表
class Posts(Base):
    __tablename__ = 'mex_post'

    # ID 主键  自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 标题 唯一 不为空
    post_title = Column(String(256), unique=True, nullable=False)
    # 特色图片
    post_poster = Column(String(256))
    # 内容 Markdown 源码 不为空
    post_markdown = Column(Text, nullable=False)  # 延迟加载,避免在列表查询时查询该字段
    # 文章状态 publish ( 发布 ) / recovery ( 回收 )
    post_status = Column(String(20), nullable=False, default='publish')
    # 内容公开度 文章公开度  public /  private
    post_openness = Column(String(16), nullable=False, default="public")
    # 文章发布时间
    created_at = Column(Integer, nullable=False, default=gettimestamp())
    # 文章修改时间
    update_at = Column(Integer, nullable=False, default=created_at)
    # 文章分类 ID
    category_id = Column(Integer, ForeignKey("mex_attribute.id"))
    # 文章tags
    tags = Column(String(256))
    # 是否置顶
    top = Column(Boolean, default=False)
    # 是否允许评论
    comment_status = Column(Boolean, default=True)
    # 内容评论数
    comment_count = Column(Integer, default=0)
    # 内容浏览数
    view_count = Column(Integer, default=0)
    # 内容点赞数
    like_count = Column(Integer, default=0)

    __mapper_args__ = {
        "order_by": created_at.desc()
    }

    def __repr__(self):
        return '<Posts %r>' % self.post_title


### 链接表
class Links(Base):
    __tablename__ = 'mex_link'

    # ID 主键 自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 名称 唯一 不为空
    name = Column(String(64), unique=True, nullable=False)
    # 图标 唯一 不为空
    poster = Column(String(256), unique=True, nullable=False)
    # url 唯一 不为空
    link = Column(String(256), unique=True, nullable=False)
    # 简介
    description = Column(Text)

    __mapper_args__ = {
        "order_by": id.desc()
    }

    def __repr__(self):
        return '<Links %r>' % self.name

### 菜单配置
class Menus(Base):
    __tablename__ = 'mex_menu'
    # ID 主键 自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 名称 唯一 不为空
    name = Column(String(64), nullable=False)
    # 图标 不为空
    iconCls = Column(String(64), nullable=False)
    # 链接地址 不为空
    link = Column(String(256), nullable=False)
    # 排序
    order = Column(Integer, nullable=False, default=0)
    # 父级菜单
    parent_id = Column(Integer, nullable=False, default=0)

    __mapper_args__ = {
        "order_by": order
    }

    def __repr__(self):
        return '<Menus %r>' % self.id

### 配置表
class Options(Base):
    __tablename__ = 'mex_option'

    # ID 主键 自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 参数名称 唯一 不为空
    option_name = Column(String(64), unique=True, nullable=False)
    # 参数值
    option_value = Column(Text)

    def get(self, key):
        result = self.filter(self.option_name == key).first()
        if result:
            return result.option_value
        else:
            logger.warning('未查询到 Key 为 [ {0} ] 的配置'.format(key))
            return None

    def __repr__(self):
        return '<Options %r>' % self.option_name


### 番组表
class Bangumis(Base):
    __tablename__ = 'mex_bangumi'
    # ID 主键 自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 唯一ID 防止重复添加
    season_id = Column(Integer)
    # 标题 唯一 不为空
    title = Column(String(64), unique=True, nullable=False)
    # 封面 不为空
    cover = Column(String(256), nullable=False)
    # 简介
    description = Column(String(512))
    # 总集数
    total = Column(Integer, nullable=False, default=0)
    # 观看进度
    progress = Column(Integer, nullable=False, default=0)
    # 是否看完
    finish = Column(Boolean, default=False)
    # 在线地址
    share_url = Column(String(256))
    # 添加时间 不为空
    created_at = Column(Integer, nullable=False, default=gettimestamp())

    __mapper_args__ = {
        "order_by": created_at.desc()
    }

    def __repr__(self):
        return '<Bangumis %r>' % self.title

### Movies
class Movies(Base):
    __tablename__ = 'mex_movie'

    # ID 主键 自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 名称 不为空
    name = Column(String(32), nullable=False)
    # 标题 不为空
    title = Column(String(256))
    # 女优
    female = Column(String(100))
    # 片商
    seller = Column(String(100))
    # 封面地址 不为空
    cover = Column(String(256))
    # 简介
    description = Column(Text)
    # 分类 不为空
    category = Column(String(32))
    # 图片列表
    picture = Column(Text)
    # 磁力连接
    manget_link = Column(String(256))
    # 播放地址
    play_url = Column(String(256))
    # BT 下载地址
    download_link = Column(String(256))
    # 添加时间
    created_at = Column(Integer, nullable=False, default=gettimestamp())

    __mapper_args__ = {
        "order_by": created_at.desc()
    }

    def __repr__(self):
        return '<Movies %r>' % self.name


### 管理员日志表
class Logs(Base):
    __tablename__ = 'mex_log'

    # ID 主键 自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 添加时间 不为空
    created_at = Column(Integer, nullable=False, default=gettimestamp())
    # 操作类型 例如 登录、登出、增删改查
    operate = Column(String(64), nullable=False, default='login')
    # 用户操作 不为空
    content = Column(String(256), nullable=False)
    # 客户端 IP 地址
    client_ip = Column(String(128))

    __mapper_args__ = {
        "order_by": id.desc()
    }

    def __repr__(self):
        return '<Logs %r>' % self.content