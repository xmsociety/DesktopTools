from datetime import datetime

from sqlalchemy import (
    CHAR,
    Column,
    Date,
    DateTime,
    Index,
    Integer,
    SmallInteger,
    String,
    Time,
    UniqueConstraint,
    create_engine,
    desc,
    func,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import sessionmaker

from args import args

time_now = func.datetime("now", "localtime") if args.localtime else func.now()
# check_same_thread 不检测是否和创建线程为同一线程--可供多线程使用
# echo 输出具体执行的sql语句
engine = create_engine(
    "sqlite:///myData.db?check_same_thread=False", echo=bool(args.debug)
)

# 增查改删（CRUD）操作需要使用session进行操作
Session = sessionmaker(bind=engine)

# 基本映射类,子孙们都需要继承它
Base = declarative_base()
"""
# 查看映射对应的表
KeyMouse.__table__

# 创建数据表。一方面通过engine来连接数据库, 另一方面根据哪些类继承了Base来决定创建哪些表
# checkfirst=True, 表示创建表前先检查该表是否存在, 如同名表已存在则不再创建。其实默认就是True
Base.metadata.create_all(engine, checkfirst=True)

# 上边的写法会在engine对应的数据库中创建所有继承Base的类对应的表, 但很多时候很多只是用来则试的或是其他库的
# 此时可以通过tables参数指定方式, 指示仅创建哪些表
# Base.metadata.create_all(engine,tables=[Base.metadata.tables['keymouse']],checkfirst=True)
# 在项目中由于model经常在别的文件定义, 没主动加载时上边的写法可能写导致报错, 可使用下边这种更明确的写法
# KeyMouse.__table__.create(engine, checkfirst=True)

# 另外我们说这一步的作用是创建表, 当我们已经确定表已经在数据库中存在时, 我完可以跳过这一步
# 针对已存放有关键数据的表, 或大家共用的表, 直接不写这创建代码更让人心里踏实

所以我就不写了,结果不是默认执行的,所以再加上吧...

# 反向生成代码
# sqlacodegen mysql+pymysql://user:password@localhost/dbname [--tables table_name1,table_name2] [--outfile model.py]
"""


# 定义键盘鼠标事件类KeyMouse,其继承上一步创建的Base
class KeyMouse(Base):
    """

    # 如果有多个类指向同一张表,那么在后边的类需要把extend_existing设为True,表示在已有列基础上进行扩展
    # 或者换句话说,sqlalchemy允许类是表的子集
    # __table_args__ = {'extend_existing': True}
    # 如果表在同一个数据库服务(datebase)的不同数据库中(schema),可使用schema参数进一步指定数据库
    # __table_args__ = {'schema': 'test_database'}

    # 各变量名一定要与表的各字段名一样,因为相同的名字是他们之间的唯一关联关系
    # 从语法上说,各变量类型和表的类型可以不完全一致,如表字段是String(64),但我就定义成String(32)
    # 但为了避免造成不必要的错误,变量的类型和其对应的表的字段的类型还是要相一致

    # sqlalchemy强制要求必须要有主键字段不然会报错,如果要映射一张已存在且没有主键的表,那么可行的做法是将所有字段都设为primary_key=True
    # 不要看随便将一个非主键字段设为primary_key,然后似乎就没报错就能使用了,sqlalchemy在接收到查询结果后还会自己根据主键进行一次去重
    """

    # 指定本类映射到`keymouse`表
    __tablename__ = "keymouse"

    # 指定id映射到id字段; id字段为整型,为主键,自动增长(其实整型主键默认就自动增长)
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 指定name映射到name字段; name字段为字符串类形
    name = Column(CHAR(1), nullable=False)
    create_time = Column(
        DateTime(timezone=8), server_default=time_now, comment="创建时间 datetime"
    )
    update_time = Column(
        DateTime, server_default=time_now, onupdate=time_now, comment="修改时间"
    )
    count = Column(Integer, server_default=text("1"), comment="次数统计")
    device = Column(
        SmallInteger, nullable=False, server_default=text("0"), comment="设备1: 键盘, 0: 鼠标"
    )
    UniqueConstraint("name", "create_time", name="fcx_name_date")

    # __repr__方法用于输出该类的对象被print()时输出的字符串,如果不想写可以不写
    def __repr__(self):
        return "<KeyMouse(name='%s', create_time='%s', count='%d')>" % (
            self.name,
            datetime2str(self.create_time),
            self.count,
        )


# 定义工作时间状态类WorkInfo
class WorkInfo(Base):
    """
    pass
    """

    __tablename__ = "workinfo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(SmallInteger, server_default=text("1"), comment="类型, 见 type_map")
    continued = Column(
        Integer, nullable=False, comment="此条状态持续时间,create_time-continued为这条状态真正开始时间"
    )
    star = Column(SmallInteger, server_default=text("0"), comment="星级, 允许收藏一些东西")
    create_time = Column(
        DateTime(timezone=8),
        server_default=time_now,
        comment="创建时间 datetime, 在状态结束/状态切换时才会插入",
    )
    update_time = Column(
        DateTime, server_default=time_now, onupdate=time_now, comment="修改时间"
    )
    note = Column(String, comment="笔记,比如小憩前可以先记录一下当前工作的进度.提醒性文字,再小憩")
    UniqueConstraint("type", "create_time", name="notefx_type_crtime")
    Index("date_max", "create_time", "continued")

    type_map = {1: "工作", 2: "开会", -1: "小憩", -2: "午休"}
    type_map_reverse = dict(zip(type_map.values(), type_map.keys()))

    @hybrid_property
    def name(self):
        # 返回值中可获取name
        return self.type_map(self.type)

    @hybrid_method
    def point_type(self, _type):
        # 大则大,小则小,无则全
        if _type > 0:
            return self.type > _type
        elif _type < 0:
            return self.type < _type
        else:
            return True

    def __repr__(self):
        return "<WorkInfo(name='%s', create_time='%s', type='%d')>" % (
            self.name,
            datetime2str(self.create_time),
            self.type,
        )


WorkInfo.__table__.create(engine, checkfirst=True)
KeyMouse.__table__.create(engine, checkfirst=True)
