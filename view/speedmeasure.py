# -*- coding: UTF-8 -*-
"""
create: 2022年10月23日09:16:23
author：moubiao wensujian
fuction:
update:
"""
import re
import time
import os
import time
from flask import Flask,jsonify,request,render_template,flash,redirect,url_for,send_from_directory,session,make_response,Blueprint
from werkzeug.utils import secure_filename
import sqlite3
import platform
import cv2
import numpy as np
import shutil

UPLOAD_FOLDER = 'upload/'
ALLOWED_EXTENSIONS = {'mp4'}
FRAME_NUM = 10 #全局变量设置每秒拆帧数

speedmeasure = Blueprint('speedmeasure', __name__, url_prefix='/speedmeasure')


@speedmeasure.route('/getFunctionByProjId', methods=['GET', 'POST'])
def getFunctionByProjectId():
    project_id = request.values.get("Value")
    functions = []
    if request.method == 'GET':
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = f"SELECT function,id FROM functions WHERE status==1 and project_id={project_id}"
                print(command)
                cur.execute(command)
                rows = cur.fetchall()
                for row in rows:
                    functions.append(row)
                return jsonify({"code": "200", "functions": functions})
        except Exception as e:
            print(e)
            return jsonify({"code": "500"})
        finally:
            con.close()


@speedmeasure.route('/getProject', methods=['GET', 'POST'])
def getPro():
    projects = []
    if request.method == 'GET':
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = "SELECT project,id FROM projects WHERE status==1"
                print(command)
                cur.execute(command)
                rows = cur.fetchall()
                for row in rows:
                    projects.append(row)
                return jsonify({"code": "200", "projects": projects})
        except Exception as e:
            print(e)
            return jsonify({"code": "500"})
        finally:
            con.close()

@speedmeasure.route('/save', methods=['GET', 'POST'])
def saveResult():
    if request.method == 'POST':
        project_id = request.values.get("project_id")
        function_id = request.values.get("function_id")
        duration = request.values.get("duration")
        timestamp = request.values.get("timestamp")
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = f"INSERT INTO result (function_id, duration, \"timestamp\") VALUES ({function_id},{duration},{timestamp});".replace('\\','')
                print(command)
                cur.execute(command)
                con.commit()
                return jsonify({"code": "200"})
        except Exception as e:
            print(e)
            return jsonify({"code": "500"})
        finally:
            con.close()

"""展示speedmeasure页面"""
@speedmeasure.route('/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def sm():
    return render_template('speedmeasure.html')

"""点击计算，计算时间"""
@speedmeasure.route('/measure', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def measure():
    start_photo_number = request.values.get("startFrame")
    end_photo_number = request.values.get("endFrame")
    Interval = (int(end_photo_number)-int(start_photo_number)) * int(1000/FRAME_NUM)
    return jsonify({"code": "200", "result": Interval, "msg": "计算完成"})

@speedmeasure.route('/uploader', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        print(request.files)
        if allowed_file(f.filename):
            f.save(os.path.join('upload/', f.filename))
            imgfile = split_video(os.path.join('upload/', f.filename))
            if imgfile != "":
                return render_template('speedmeasure.html',imgfile=imgfile)
            else:
                split_error = '文件解析失败，请检查视频文件内容和ffmpeg配置！'
                return render_template('speedmeasure.html', split_error=split_error)
        else:
            error = '文件上传失败，请检查文件类型!'
            return render_template('speedmeasure.html', error=error)
    else:
        return render_template('speedmeasure.html')


@speedmeasure.route('/smartSelect', methods=['GET', 'POST'])
def smartSel():
    if request.method == 'POST':
        function_id = request.values.get("function_id")
        imagePath = request.values.get("imagePath")
        imageNum = request.values.get("imageNum")
        startFrame = 0
        endFrame = 0
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = f"SELECT function,project_id FROM functions WHERE status==1 and id={function_id}"
                print(command)
                cur.execute(command)
                result = cur.fetchone()
                project_id = result[1]
                baseline_start_frame = "./baseline/" + str(project_id) + "_" + str(function_id) + "_" +"start.png"
                baseline_end_frame = "./baseline/" + str(project_id) + "_" + str(function_id) + "_" + "end.png"
                threshold = 0.9
                start_similarity = []
                start_similarity.append(0)
                end_similarity = []
                end_similarity.append(0)
                #比较基线与开始帧间的相似度
                for i in range(1,int(imageNum)+1):
                    target_frame = imagePath + "/" + str(i) + ".png"
                    target_frame = target_frame[1:] #特殊处理，修改相对路径
                    similarity = classify_hist_with_split(baseline_start_frame,target_frame, size=(256, 256))
                    #print('三直方图算法相似度：', similarity)
                    start_similarity.append(similarity)
                print(start_similarity)
                # 比较基线与结束帧间的相似度
                for i in range(1, int(imageNum) + 1):
                    target_frame = imagePath + "/" + str(i) + ".png"
                    target_frame = target_frame[1:] #特殊处理，修改相对路径
                    similarity = classify_hist_with_split(baseline_end_frame, target_frame, size=(256, 256))
                    end_similarity.append(similarity)
                print(end_similarity)
                # 找开始帧，需要先找到与开始帧最相似的一帧，跳过前面可能存在的无关帧（多录制了一段视频）
                max_similarity_index = 0
                max_similarity = 0
                for i in range(1, int(imageNum) + 1):
                    if start_similarity[i] > max_similarity:
                        max_similarity_index = i
                        max_similarity = start_similarity[i]
                # print(max_similarity)
                # print(max_similarity_index)

                while threshold >= 0.1:
                    print('阀值：', threshold)
                    start_threshold = threshold
                    end_threshold = threshold

                    # if threshold < 0.5:
                    #     start_threshold = 0.50
                    #根据基线，寻找开始帧
                    for i in range(max_similarity_index,int(imageNum)+1):
                        if start_similarity[i] < start_threshold:
                            if startFrame == 0:
                                startFrame = i - 1
                            print('找到开始帧：', startFrame)
                            break
                    # 根据基线，寻找结束帧
                    for i in range(1, int(imageNum) + 1):
                        if end_similarity[i] > end_threshold:
                            if endFrame == 0:
                                endFrame = i
                            print('找到结束帧：', endFrame)
                            break
                    if startFrame != 0 and endFrame != 0:
                        #找到了开始帧和结束帧
                        break
                    threshold -= 0.02

                #判断是否成功找到开始帧和结束帧
                if startFrame != 0 and endFrame != 0:
                    return jsonify({"code": "200", "startFrame": startFrame,"endFrame": endFrame})
                else:
                    return jsonify({"code": "500"})
        except Exception as e:
            print(e)
            return jsonify({"code": "500"})
        finally:
            con.close()

@speedmeasure.route('/base', methods=['GET', 'POST'])
def saveBase():
    if request.method == 'POST':
        function_id = request.values.get("function_id")
        startFrame = request.values.get("startFrame")
        endFrame = request.values.get("endFrame")
        imagePath = request.values.get("imagePath")
        try:
            with sqlite3.connect("./SpeedMeasure.db") as con:
                cur = con.cursor()
                command = f"SELECT function,project_id FROM functions WHERE status==1 and id={function_id}"
                print(command)
                cur.execute(command)
                result = cur.fetchone()
                function_name = result[0]
                project_id = result[1]
                command = f"SELECT project FROM projects WHERE status==1 and id={project_id}"
                print(command)
                cur.execute(command)
                result = cur.fetchone()
                project_name = result[0]
                baseline_start_frame = "./baseline/" + str(project_id) + "_" + str(function_id) + "_" + "start.png"
                baseline_end_frame = "./baseline/" + str(project_id) + "_" + str(function_id) + "_" + "end.png"
                startFrame_path = imagePath + "/" + startFrame + ".png"
                startFrame_path = startFrame_path[1:]  #特殊处理，修改相对路径
                endFrame_path = imagePath + "/" + endFrame + ".png"
                endFrame_path = endFrame_path[1:]  #特殊处理，修改相对路径

                shutil.copyfile(startFrame_path,baseline_start_frame)
                shutil.copyfile(endFrame_path,baseline_end_frame)

                return jsonify({"code": "200"})
        except Exception as e:
            print(e)
            con.rollback()
            return jsonify({"code": "500"})
        finally:
            con.close()


#---------------------------------------拆分视频-------------------------------------------------
def split_video(video_path):
    timestamp = str(int(round(time.time() * 1000)))
    path_photo = "./static/" + timestamp
    os.makedirs(path_photo)
    file_count = 0
    try:
        sysstr = platform.system()
        if sysstr =="Windows":
            command = r"ffmpeg.exe -i {audio_path} -r {frame_num} {path_photo}/%d.png".format(
                        audio_path=video_path, frame_num = FRAME_NUM,path_photo=path_photo)
        else:
            command = r"./ffmpeg -i {audio_path} -r {frame_num} {path_photo}/%d.png".format(
                audio_path=video_path, frame_num = FRAME_NUM,path_photo=path_photo)
        os.system(command)
        for root, dir, files in os.walk(path_photo):
            file_count = len(files)
        #检查视频是否成功解析
        if file_count == 0:
            return ""
    except Exception as e:
        print(e)
    return "../static/"+timestamp+"-"+str(file_count)

def allowed_file(filename):
    """
    判定文件的有效性
    params filename：上传文件的名称
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#------------------------------图像识别代码------------------------------------------------
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # RGB每个通道的直方图相似度
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.imread(image1)
    image2 = cv2.imread(image2)
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data

def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                     (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree