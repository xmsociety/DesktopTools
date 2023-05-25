from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    SmallInteger,
    String,
    create_engine,
    func,
    text,
)
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import sessionmaker

from ..args import args
from ..tools import datetime2str

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


class FuncClass(BaseModel):
    class A:
        def _func(self):
            pass
    desc: str
    result: str = ''
    func: type(A()._func)

    class Config:
        arbitrary_types_allowed = True

    def get_result(self, text):
        ok, rst = self.func(text)
        if ok:
            self.result = ": ".join((self.desc, rst))
        return ok


# 定义工作时间状态类WorkInfo
class KVMap(Base):
    """
    pass
    """

    __tablename__ = "kvmap"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(
        SmallInteger,
        server_default=text("1"),
        comment="类型, 见 type_map"
    )
    create_time = Column(
        DateTime(timezone=8),
        server_default=time_now,
        comment="创建时间 datetime",
    )
    key = Column(String, comment="Key")
    value = Column(String, comment="Value")
    Index("key", )

    type_map = {1: "文本", 2: "url", 3: "file path", 4: "img path"}
    type_map_reverse = dict(zip(type_map.values(), type_map.keys()))

    def __repr__(self):
        return "<KVMap(id='%s', key='%s', create_time='%s')>" % (
            self.id,
            self.key,
            datetime2str(self.create_time),
        )


KVMap.__table__.create(engine, checkfirst=True)
