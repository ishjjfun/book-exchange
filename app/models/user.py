from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from flask_login import UserMixin
from app import login_manager
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    _password = Column('password', String(128))
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        gifting = Gift.query.fliter_by(uid=self.id, isbn=isbn,
                                       launched=False).firet()
        wishing = Wish.query.fliter_by(uid=self.id, isbn=isbn,
                                       launched=False).firet()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def rest_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
