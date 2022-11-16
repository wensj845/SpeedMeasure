#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: wensujian, huangkai
# create: 2022年11月6日20:35:23

from flask import Flask, jsonify, request, render_template, flash, redirect, url_for, send_from_directory, session, \
    make_response, Blueprint
import sqlite3

history = Blueprint('history', __name__, url_prefix='/history')

"""历史记录"""


@history.route('/', methods=['GET', 'POST'])
def report():
    out_html = render_template("history.html", rows=getProjcts())
    return out_html, "200 Ok", {"Content-type": "text/html"}


@history.route('/functions', methods=['GET', 'POST'])
def getfunctions():
    pro_id = request.values.get("pro_id")
    functions = []
    if request.method == 'GET':
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = """SELECT result.project,result.function,result.timestamp,result.id,count(*),
                result.duration,result.duration FROM (select projects.project,functions.function,
                result.function_id,result.duration,result.timestamp,functions.id from projects,functions,result where 
                projects.status = 1 and functions.status = 1 and projects.id in ({pro_id}) and projects.id = 
                functions.project_id and result.function_id = functions.id order by timestamp desc) as result GROUP 
                BY result.function_id""".format(pro_id=pro_id)
                cur.execute(command)
                rows = cur.fetchall()
                for row in rows:
                    functions.append(row)
                return jsonify({"code": "200", "functions": functions})
        except Exception as e:
            con.rollback()
            return jsonify({"code": "500"})
        finally:
            con.close()


@history.route('/results', methods=['GET', 'POST'])
def getResults():
    func_id = request.values.get("func_id")
    results = []
    if request.method == 'GET':
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = """SELECT fun.function,rt.duration,rt.timestamp,pro.project,rt.id,fun.id FROM functions fun,result rt,
                projects pro WHERE rt.function_id = fun.id AND rt.function_id in ({func_id}) AND fun.project_id = 
                pro.id AND fun.status = 1 AND pro.status = 1 ORDER BY rt.timestamp DESC""".format(func_id=func_id)
                cur.execute(command)
                rows = cur.fetchall()
                for row in rows:
                    results.append(row)
                return jsonify({"code": "200", "functions": results})
        except Exception as e:
            con.rollback()
            return jsonify({"code": "500"})
        finally:
            con.close()


@history.route('/allData', methods=['GET', 'POST'])
def getAllData():
    results = []
    project_id = request.values.get("project_id")
    if request.method == 'GET':
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = """SELECT fun.function,rt.duration,rt.timestamp,pro.project FROM functions fun,result rt,
                projects pro WHERE rt.function_id = fun.id AND fun.project_id = pro.id AND pro.id in ({project_id}) 
                ORDER BY rt.timestamp DESC""".format(project_id=project_id)
                cur.execute(command)
                rows = cur.fetchall()
                for row in rows:
                    results.append(row)
                return jsonify({"code": "200", "allData": results})
        except Exception as e:
            con.rollback()
            return jsonify({"code": "500"})
        finally:
            con.close()


@history.route('/defaultPro', methods=['GET', 'POST'])
def getdefaultPro():
    results = []
    if request.method == 'GET':
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = """SELECT pro.id FROM functions fun,projects pro WHERE fun.project_id = pro.id AND 
                fun.status = 1  AND pro.status = 1 GROUP BY pro.id """
                cur.execute(command)
                rows = cur.fetchall()
                results.append(rows[0][0])
                return jsonify({"code": "200", "defaultPro": results})
        except Exception as e:
            con.rollback()
            return jsonify({"code": "500"})
        finally:
            con.close()


@history.route('/del', methods=['POST'])
def delrt():
    rtid = request.form.get('rtid')
    try:
        with sqlite3.connect("./SpeedMeasure.db") as con:
            cur = con.cursor()
            command = """
                    delete 
                    from 
                        result 
                    where
                        result.id = '{rtid}'
                """.format(rtid=rtid)
            cur.execute(command)
            # one = cur.fetchone()
            return jsonify({"code": "200", "mg": "删除成功"})
    except Exception as e:
        print(e)
        con.rollback()
        return jsonify({"code": "500"})
    finally:
        con.close()


def getProjcts():
    con = sqlite3.connect("./SpeedMeasure.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from projects where status==1")
    rows = cur.fetchall()
    con.close()
    return rows
