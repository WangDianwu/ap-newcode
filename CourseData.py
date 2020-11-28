#开课数据管理
import string

import xlrd as xlrd
from flask import Flask, redirect, url_for, request, Response, render_template, flash, session,Blueprint
from sql.sqlite3 import *
import json
import time

#模块
coursedata_api = Blueprint("coursedata_api",__name__)


#将所有的教师授课信息显示出来
@coursedata_api.route('/course', methods=['POST', 'GET'])
def course():
    r = request.args.get('result', '')
    #查询教师授课表
    result,_ = GetSql2("select * from t_teaching")
    #查询开课班级表
    for i in range(len(result)):
        result1, _ = GetSql2("select calss_name from t_open_class, t_class_info where t_open_class.class_num = t_class_info.class_num and course_num = '"+str(result[i][0])+"' and course_id = '"+str(result[i][1])+"'")
        result[i] = (result[i], result1)
    return render_template("man_cou_cap.html", results=result, result=r)

#查询开设课程
@coursedata_api.route('/selectCourse', methods=['POST'])
def selectCourse():
    r = request.args.get('result', '')
    kehao = request.form.get('kehao')
    kexuhao = request.form.get('kexuhao')
    strsql="select * from t_teaching where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"'"
    if  kexuhao=="" :
        strsql="select * from t_teaching"
    # 查询教师授课表
    result, _ = GetSql2(strsql)
    # 查询开课班级表
    for i in range(len(result)):
        result1, _ = GetSql2("select calss_name from t_open_class, t_class_info where t_open_class.class_num = t_class_info.class_num and course_num = '" + str(
            result[i][0]) + "' and course_id = '" + str(result[i][1]) + "'")
        result[i] = (result[i], result1)
    return render_template("man_cou_cap.html", results=result, result=r)

@coursedata_api.route('/add_open', methods=['POST', 'GET'])
def add_open():
    #添加开设课程页面
    #把没有开课的课程编号传过去
    kehao, _ = GetSql2("select course_num from t_course_info where course_num not in (select course_num from t_teaching)")
    #查询所有的教师编号传过去
    tea, _ = GetSql2("select teacher_num from t_teacher_info")
    #查询所有的班级
    ban, _ = GetSql2("select class_num from t_class_info")

    return render_template("add_open_cap.html", kehao=kehao, tea=tea, ban=ban)

#添加开设课程
@coursedata_api.route('/addCoursedata', methods=['POST', 'GET'])
def addCoursedata():
    if request.method == 'POST':
        #获取信息
        kehao = request.form.get('kehao')
        kexuhao = request.form.get('kexuhao')
        tea = request.form.get('tea')
        num = request.form.get('num')
        kaike = request.form.get('kaike')
        didian = request.form.get('didian')
        zhou = request.form.get('zhou')
        xing = request.form.get('xing')
        jie = request.form.get('jie')
        opens = request.form.getlist('open')
        #将开课信息存储到数据库
        data = dict(
            course_num = kehao,
            course_id = kexuhao,
            teacher_num = tea,
            teaching_max = num,
            open_date = kaike,
            class_addr = didian,
            weeks_count =zhou,
            week_num = xing,
            sections_num = jie
        )
        result = InsertDataOne(data, "t_teaching")
        print(result)
        for o in opens:
            data1 = dict(course_num=kehao, course_id=kexuhao, class_num=o)
            resulta= InsertDataOne(data1, "t_open_class")
            print(resulta)
        return redirect(url_for('coursedata_api.course', result=result))
    else:
        return redirect(url_for('coursedata_api.course'))

    
#删除开设课程
@coursedata_api.route('/deleteCourcedata', methods=['GET', 'POST'])
def deleteCourcedata():
    if request.method == 'GET':
        kehao = request.args.get('kehao')
        kexuhao = request.args.get('kexuhao')
        tea = request.args.get('tea')
        sql1 = "delete from t_teaching where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"' and teacher_num = '"+str(tea)+"'"
        result1 = DelDataByIdOne(sql1)
        sql2 = "delete from t_open_class where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"'"
        result2 = DelDataByIdOne(sql2)
        if result1 == '删除成功' and result2 == '删除成功':
            result = '删除成功'
        else:
            result = '删除失败'
        return redirect(url_for('coursedata_api.course', result=result))
    else:
        #批量删除
        couids = request.form.getlist('couid')
        ke = []
        flag = 0
        for couid in couids:
            index = couid.find('+')
            index2 = couid.find('+', index+1)
            dic = {}
            dic['kehao'] = couid[:index]
            dic['kexuhao'] = couid[index + 1:index2]
            dic['tea'] = couid[index2+1:]
            #删除数据
            result1 = DelDataByIdOne("delete from t_teaching where course_num = '"+str(dic['kehao'])+"' and course_id = '"+str(dic['kexuhao'])+"' and teacher_num = '"+str(dic['tea'])+"'")
            result2 = DelDataByIdOne("delete from t_open_class where course_num = '"+str(dic['kehao'])+"' and course_id = '"+str(dic['kexuhao'])+"'")
            if result1 == '删除成功' and result2 == '删除成功':
                continue
            else:
                flag = 1
        if flag == 1:
            result = '删除失败'
        else:
            result = '删除成功'
        return redirect(url_for('coursedata_api.course', result=result))

#修改开设课程页面
@coursedata_api.route('/updateCourcePagedata', methods=['GET'])
def updateCourcePagedata():
    #将数据查询出来，传递给修改界面
    kehao = request.args.get('kehao')
    kexuhao = request.args.get('kexuhao')
    tea = request.args.get('tea')

    # #添加开设课程页面
    # #把没有开课的课程编号传过去
    teaching, _ = GetSql2("select * from t_teaching where course_num ='"+kehao+"' and course_id='"+kexuhao+"'" )
    openclass, _ = GetSql2("select * from t_open_class where course_num ='"+kehao+"' and course_id='"+kexuhao+"'")
    print(teaching)
    print(openclass)
    #查询所有的教师编号传过去
    tea, _ = GetSql2("select teacher_num from t_teacher_info")
    #查询所有的班级
    ban, _ = GetSql2("select class_num from t_class_info")

    return render_template("updateCourcePagedata_cap.html", kehao=kehao, kexuhao=kexuhao,tea=tea, ban=ban,teaching=teaching,openclass=openclass)


#修改开设课程
@coursedata_api.route('/updateCoursedata', methods=['POST', 'GET'])
def updateCoursedata():
    if request.method == 'POST':
        #获取信息
        course_num = request.form.get('kehao')
        course_id = request.form.get('kexuhao')
        teacher_num = request.form.get('tea')
        teaching_max = request.form.get('num')
        open_date = request.form.get('kaike')
        class_addr = request.form.get('didian')
        weeks_count = request.form.get('zhou')
        week_num = request.form.get('xing')
        sections_num = request.form.get('jie')
        class_num = request.form.getlist('open')

        sql = "update t_teaching set teacher_num ='"+str(teacher_num)+"',teaching_max ='"+str(teaching_max)+"',open_date ='"+str(open_date)+"',class_addr ='"+str(class_addr)+"' ,weeks_count ='"+str(weeks_count)+"' ,week_num ='"+str(week_num)+"' ,sections_num ='"+str(sections_num)+"' where course_num ='"+str(course_num)+"' and course_id ='"+str(course_id)+"'"
        result = UpdatedataTwo(sql) 
        print(result)
        # 修改开课班级 先删了 再添加
        sql2 = "delete from t_open_class where  course_num ='"+str(course_num)+"' and course_id ='"+str(course_id)+"'"
        result1 = UpdatedataTwo(sql2) 
        print(result1)
        for o in class_num:
            data1 = dict(course_num=course_num, course_id=course_id, class_num=o)
        resulta= InsertDataOne(data1, "t_open_class")
        print(resulta)
        return redirect(url_for('coursedata_api.course', result=result))
    else:
        return redirect(url_for('coursedata_api.course'))

