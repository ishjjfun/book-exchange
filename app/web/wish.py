from flask import flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.wish import MyWishes
from . import web

__author__ = '七月'


@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    wishes_of_mime = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mime]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyWishes(wishes_of_mime, gift_count_list)
    return render_template('my_wish.html', gifts=view_model.gifts)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.id = current_user.id
            db.session.add(gift)
    else:
        flash('这本书已添加到赠送清单或心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
