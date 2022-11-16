# -*- coding: UTF-8 -*-
"""
create: 2022年11月14日12:30:23
author：moubiao, huangkai
fuction:
update:
"""

import os
from flask import Flask, request, session
from datetime import timedelta

from werkzeug.utils import redirect

from view.index import web
from view.speedmeasure import speedmeasure
from view.user import user
from view.setting import setting
from view.history import history
from view.auth import auth

UPLOAD_FOLDER = '/uploads'
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SECRET_KEY'] = os.urandom(24)  ## 加密session中的 secret_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # 持久化时间设置

##注册蓝图
app.register_blueprint(web)
app.register_blueprint(speedmeasure)
app.register_blueprint(user)
app.register_blueprint(setting)
app.register_blueprint(history)
app.register_blueprint(auth)


@app.before_request
def before():
    print(request.path)

    if request.path == "/":
        return None
    if request.path.startswith("/static"):
        return None
    if request.path == "/login":
        if session.get("user_info"):
            return redirect("/speedmeasure")
        return None
    if request.path == "/login/":
        if session.get("user_info"):
            return redirect("/speedmeasure")
        return None
    if request.path == "/auth/register":
        return None
    if request.path == "/auth/doRegister":
        return None
    if request.path == "/auth/validate":
        return None
    if not session.get("user_info"):
        return redirect("/")
    if request.path.startswith("/setting"):
        if session.get("user_admin") == 0:
            return redirect("/speedmeasure")
        return None


if __name__ == "__main__":
    app.run(port=12355, host="127.0.0.1", debug=False)
