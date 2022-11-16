# -*- coding: UTF-8 -*-
"""
create: 2022年10月23日09:16:23
author：moubiao wensujian
fuction:
update:
"""
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for, send_from_directory, session, \
    make_response, Blueprint
import sqlite3

setting = Blueprint('setting', __name__, url_prefix='/setting')

"""设置页面"""


@setting.route('/', methods=['GET', 'POST'])
def config():
    if request.method == 'GET':
        return render_template("setting.html", rows=getProjcts())


@setting.route('/project', methods=['GET', 'POST'])
def addProject():
    if request.method == 'POST':
        projects = []
        project = request.values.get("project")
        print(project)
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = "INSERT INTO projects (project,status) VALUES('{project}',1)".format(project=project)
                print(command)
                cur.execute(command)
                con.commit()
        except Exception as e:
            con.rollback()
            print(e)
            return jsonify({"code": "500"})
        finally:
            con.close()
            rows = getProjcts()
            for row in rows:
                print(row[1])
                projects.append(row[1])
            return jsonify({"code": "200", "projects": projects})


@setting.route('/function', methods=['GET', 'POST'])
def addFunction():
    if request.method == 'POST':
        project = request.values.get("project")
        function = request.values.get("function")
        print(project)
        print(function)
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = "select id from projects where project = '{project}'".format(project=project)
                print(command)
                cur.execute(command)
                project_id = cur.fetchone()[0]
                print(project_id)
                command = "INSERT INTO functions (project_id,function,status) VALUES({project_id},'{function}',1)".format(
                    project_id=project_id, function=function)
                print(command)
                cur.execute(command)
                con.commit()
                return jsonify({"code": "200"})
        except Exception as e:
            con.rollback()
            print(e)
            return jsonify({"code": "500"})
        finally:
            con.close()


@setting.route('/delf', methods=['GET', 'POST'])
def delf():
    if request.method == 'POST':
        fuc_id = request.values.get("fuc_id")
        print(fuc_id)
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = "UPDATE functions SET status=0 WHERE id={fuc_id}".format(fuc_id=fuc_id)
                print(command)
                cur.execute(command)
                con.commit()
                return jsonify({"code": "200"})
        except Exception as e:
            con.rollback()
            print(e)
            return jsonify({"code": "500"})
        finally:
            con.close()


@setting.route('/delp', methods=['GET', 'POST'])
def delp():
    if request.method == 'POST':
        pro_id = request.values.get("pro_id")
        print(pro_id)
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = "UPDATE projects SET status=0 WHERE id={pro_id}".format(pro_id=pro_id)
                print(command)
                cur.execute(command)
                command = "UPDATE functions SET status=0 WHERE project_id={pro_id}".format(pro_id=pro_id)
                print(command)
                cur.execute(command)
                con.commit()
                return jsonify({"code": "200"})
        except Exception as e:
            con.rollback()
            print(e)
            return jsonify({"code": "500"})
        finally:
            con.close()


@setting.route('/getProjectsAndFunctions', methods=['GET', 'POST'])
def getProjectsAndFunctions():
    projects = []
    functions = []
    function_ids = []
    project_ids = []
    if request.method == 'GET':
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = "SELECT p.project,f.function,f.id FROM projects p,functions f WHERE p.id == f.project_id AND f.status==1"
                print(command)
                cur.execute(command)
                rows = cur.fetchall()
                for row in rows:
                    projects.append(row[0])
                    functions.append(row[1])
                    function_ids.append(row[2])
                return jsonify(
                    {"code": "200", "projects": projects, "functions": functions, "function_ids": function_ids})
        except Exception as e:
            con.rollback()
            print(e)
            return jsonify({"code": "500"})
        finally:
            con.close()


@setting.route('/getPro', methods=['GET', 'POST'])
def getPro():
    projects = []
    project_ids = []
    if request.method == 'GET':
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = "SELECT project,id FROM projects WHERE status==1"
                print(command)
                cur.execute(command)
                rows = cur.fetchall()
                for row in rows:
                    projects.append(row[0])
                    project_ids.append(row[1])
                return jsonify({"code": "200", "projects": projects, "project_ids": project_ids})
        except Exception as e:
            con.rollback()
            print(e)
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
