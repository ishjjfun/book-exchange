from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    # autoincrement根据记录数自增长
    title = Column(String(50), nullable=False)
    # nullable为不为空
    author = Column(String(30), default='未命名')
    # default默认值
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    # unique重复不重复
    summary = Column(String(1000))
    image = Column(String(50))


    def sample(self):
        pass
