# -*- coding: UTF-8 -*-
"""
create: 2022年10月23日09:16:23
author：moubiao
fuction:
update:
"""

from datetime import timedelta, datetime
from flask import Flask,jsonify,request,render_template,flash,redirect,url_for,send_from_directory,session,make_response,Blueprint

user = Blueprint('user', __name__, url_prefix='/user')

"""图片显示"""
@user.route('/display/img/<string:filename>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def display_img(filename):
    out_html = render_template("photo.html")
    return out_html, "200 Ok", {"Content-type": "text/html"}
