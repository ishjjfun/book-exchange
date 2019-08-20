from flask import Blueprint, render_template

web = Blueprint('web', __name__)
# 第一个参数蓝图名称，二：蓝图所在的包或模块


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


from app.web import test
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
