# -*- coding: UTF-8 -*-
"""
create: 2022年10月23日09:16:23
author：moubiao,huangkai
fuction:
update:
"""

import re
import os
import sqlite3
import hashlib

from flask import jsonify, request, render_template, flash, redirect, url_for, send_from_directory, session, \
    make_response, Blueprint

web = Blueprint('web', __name__)


@web.route('/', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def index():
    out_html = render_template("login.html")
    return out_html, "200 Ok", {"Content-type": "text/html"}


@web.route('/login/', methods=['POST'])
def login():
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    session.permanent = True
    try:
        with sqlite3.connect("./SpeedMeasure.db") as con:
            cur = con.cursor()
            command = """
                    select 
                        count(*),
                        * 
                    from 
                        user 
                    where
                        email = '{email}'
                    and
                        password = '{pwd}'
                """.format(email=email, pwd=loadMd5(pwd))
            cur.execute(command)
            one = cur.fetchone()

            # session状态维护
            if one[0] == 1:
                name = loadUserName(cur, email)
                session['user_info'] = email
                session['user_name'] = name
                session['user_admin'] = one[5]
                out_html = render_template("speedmeasure.html")
                return out_html, "200 Ok", {"Content-type": "text/html"}
            else:
                return render_template('login.html', msg='用户名或密码输入错误', email=email, pwd=pwd)
    except Exception as e:
        print(e)
        con.rollback()
        return jsonify({"code": "500"})
    finally:
        con.close()


def loadUserName(cur, email):
    comm = """
        select 
            username
        from
            user
        where
            email = '{email}'
    """.format(email=email)
    cur.execute(comm)
    one = cur.fetchone()
    return one[0]


def loadMd5(src):
    m2 = hashlib.md5()
    m2.update(src.encode())
    return m2.hexdigest()

# """登录退出"""
# @web.route('/login/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
# def login():
#     if request.method=='GET':
#         return  render_template('speedmeasure.html')
#     # session  字典类型     登录操作，记录信息传输到数据库
#     user=request.form.get('email')
#     pwd=request.form.get('pwd')
#     session['username'] = user
#     session['user_id'] = pwd
#     # 持久化  有效期
#     session.permanent = True
#
#     if user == user and pwd == pwd:
#         session['user_info'] = user
#         out_html = render_template("speedmeasure.html")
#         return out_html, "200 Ok", {"Content-type": "text/html"}
#     else:
#         return render_template('login.html', msg='用户名或密码输入错误')

# @web.route('/logout/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
# def logout():
#     # 删除session中的username
#     session.pop('username')
#     # 清空session中的所有数据
#     session.clear()
#     return redirect('login')
#
# """用户管理"""
# @web.route("/users", methods=['GET', 'POST','PUT','PATCH','DELETE'])
# def get_all_users():
#     """获取所有用户信息"""
#     return jsonify({"code":"0", "data":datas, "msg":"操作成功"})
#
# @web.route("/users/<int:user_id>", methods=['GET', 'POST','PUT','PATCH','DELETE'])
# def get_user(user_id):
#     """获取某个用户信息"""
#     if user_id > 0 and user_id <= len(datas):
#         return jsonify({"code": "0", "data": datas[user_id - 1], "msg": "操作成功"})
#     return jsonify({"code": "1", "msg": "用户不存在"})
#
# @web.route("/practice/users/userregister", methods=['GET', 'POST','PUT','PATCH','DELETE'])
# def user_register():
#     username = request.json.get("username").strip() # 用户名
#     password = request.json.get("password").strip() # 密码
#     sex = request.json.get("sex", "0").strip() # 性别，默认为0(男性)
#     telephone = request.json.get("telephone", "").strip() # 手机号，默认为空串
#     address = request.json.get("address", "").strip() # 地址，默认为空串
#     if username and password and telephone:
#         if username == "wintest":
#             return jsonify({"code": 2002, "msg": "用户名已存在！！！"})
#         elif not (sex == "0" or sex == "1"):
#             return jsonify({"code": 2003, "msg": "输入的性别只能是 0(男) 或 1(女)！！！"})
#         elif not (len(telephone) == 11 and re.match("^1[3,5,7,8]\d{9}$", telephone)):
#             return jsonify({"code": 2004, "msg": "手机号格式不正确！！！"})
#         else:
#             return jsonify({"code": 0, "msg": "恭喜，注册成功！"})
#     else:
#         return jsonify({"code": 2001, "msg": "用户名/密码/手机号不能为空，请检查！！！"})
