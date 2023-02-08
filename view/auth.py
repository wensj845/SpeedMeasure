#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: wensujian, huangkai
# create: 2022年11月12日 11:12:23

import re
import os
import sqlite3
import hashlib

from flask import jsonify, request, render_template, flash, redirect, url_for, send_from_directory, session, \
    make_response, Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")

@auth.route('/', methods=['GET', 'POST'])
def authority():
    try:
        admin = session.get('user_admin')
        name = session.get("user_name")
        return jsonify({"code": "200", "admin": admin, "name": name})
    except Exception as e:
        print(e)
        return jsonify({"code": "500"})

@auth.route('/register', methods=['GET', 'POST'])
def register():
    out_html = render_template("register.html")
    return out_html, "200 Ok", {"Content-type": "text/html"}


@auth.route('/validate', methods=['GET', 'POST'])
def validate():
    rEmail = request.form.get('rEmail')
    try:
        with sqlite3.connect("./SpeedMeasure.db") as con:
            cur = con.cursor()
            command = """
                    select
                        count(*)
                    from
                        user
                    where
                        email = '{rEmail}'
                """.format(rEmail=rEmail)
            cur.execute(command)
            one = cur.fetchone()
            if one[0] == 0:
                return jsonify({"code": "200"})
            else:
                return jsonify({"code": "500"})

    except Exception as e:
        print(e)
        con.rollback()
        return jsonify({"code": "500"})
    finally:
        con.close()


@auth.route('/doRegister', methods=['GET', 'POST'])
def doRegister():
    rEmail = request.form.get('rEmail')
    rUser = request.form.get('rUser')
    rPwd = request.form.get('rPwd')
    raPwd = request.form.get('raPwd')

    if rPwd != raPwd:
        return render_template('register.html', msg='两次输入密码不一致请检查', rEmail=rEmail, rUser=rUser, rPwd=rPwd, raPwd=raPwd)
    try:
        with sqlite3.connect("./SpeedMeasure.db") as con:
            cur = con.cursor()
            if not validatefu(cur, rEmail):
                return render_template('register.html', msg='用户已经存在', rEmail=rEmail, rUser=rUser, rPwd=rPwd, raPwd=raPwd)
            command = """
                    INSERT INTO user (email,password,username,administrator) VALUES('{rEmail}','{rPwd}','{rUser}',0)
                """.format(rEmail=rEmail, rPwd=loadMd5(rPwd), rUser=rUser)
            print(command)
            cur.execute(command)
            con.commit()
            session['user_info'] = rEmail
            session['user_name'] = rUser
            session['user_admin'] = 0
            out_html = render_template("speedmeasure.html")
            return out_html, "200 Ok", {"Content-type": "text/html"}
    except Exception as e:
        print(e)
        con.rollback()
        if "UNIQUE constraint failed" in str(e):
            return render_template('register.html', msg='用户已经存在', rEmail=rEmail, rUser=rUser, rPwd=rPwd, raPwd=raPwd)
        return jsonify({"code": "500"})
    finally:
        con.close()


def validatefu(cur, rEmail):
    command = """
            select
                count(*)
            from
                user
            where
                email = '{rEmail}'
        """.format(rEmail=rEmail)
    cur.execute(command)
    one = cur.fetchone()
    return one[0] == 0


def loadMd5(src):
    m2 = hashlib.md5()
    m2.update(src.encode())
    return m2.hexdigest()
