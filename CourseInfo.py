import string

import xlrd as xlrd
from flask import Flask, redirect, url_for, request, Response, render_template, flash, session,Blueprint
from sql.sqlite3 import *
import json
import time

#模块
courseinfo_api = Blueprint("courseinfo_api",__name__)


#课程信息管理list
@courseinfo_api.route('/kechenglist', methods=['POST', 'GET'])
def kechenglist():
    r = request.args.get('result', '')
    #课程信息
    result,_ = GetSql2("select * from t_course_info")
    return render_template("man_kecheng_cap.html", results=result, result=r)

#查询开设课程
@courseinfo_api.route('/selectCourse1', methods=['POST'])
def selectCourse1():
    r = request.args.get('result', '')
    course_name = request.form.get('course_name')
    strsql = "select * from t_course_info where course_name='"+course_name+"'"
    #课程信息
    if course_name=='':
        strsql ="select * from t_course_info"
    result,_ = GetSql2(strsql)
    return render_template("man_kecheng_cap.html", results=result, result=r)

#跳转新增开设课程页面
@courseinfo_api.route('/add_kecheng', methods=['POST', 'GET'])
def add_kecheng():
    return render_template("add_kecheng_cap.html")

#添加开设课程
@courseinfo_api.route('/addCourse', methods=['POST', 'GET'])
def addCourse():
    if request.method == 'POST':
        #获取信息
        course_num = request.form.get('course_num')
        course_name = request.form.get('course_name')
        total_hours = request.form.get('total_hours')
        credit = request.form.get('credit')
        course_type = request.form.get('course_type')
        #将开课信息存储到数据库
        sql = "insert into t_course_info (course_num,course_name,total_hours,credit,course_type) values ('"+str(course_num)+"','"+str(course_name)+"','"+str(total_hours)+"','"+str(credit)+"','"+str(course_type)+"') "
        resultadd = InsertDataV(sql) 
        print(resultadd)
        return redirect(url_for('courseinfo_api.add_kecheng'))
    else:
        return redirect(url_for('courseinfo_api.add_kecheng'))

#修改开设课程
@courseinfo_api.route('/updateCourse', methods=['POST', 'GET'])
def updateCourse():
    if request.method == 'POST':
        #获取信息
        course_num = request.form.get('course_num')
        course_name = request.form.get('course_name')
        total_hours = request.form.get('total_hours')
        credit = request.form.get('credit')
        course_type = request.form.get('course_type')
        #将开课信息存储到数据库
        sql = "update t_course_info set course_name ='"+str(course_name)+"',total_hours ='"+str(total_hours)+"',credit ='"+str(credit)+"',course_type ='"+str(course_type)+"' where course_num ='"+str(course_num)+"'"
        result = UpdatedataTwo(sql) 
        print(sql)
        print(result)
        return redirect(url_for('courseinfo_api.kechenglist', result=result))
    else:
        return redirect(url_for('courseinfo_api.kechenglist', result="修改失败"))


#删除开设课程
@courseinfo_api.route('/deleteCource1', methods=['GET', 'POST'])
def deleteCource1():
    if request.method == 'GET':
        #单个删除
        course_num = request.args.get('course_num')
        sql = "delete from t_course_info where course_num = '"+str(course_num)+"'"
        result = DelDataByIdOne(sql)
        return redirect(url_for('courseinfo_api.kechenglist', result=result))
    else:
        #批量删除
        couids = request.form.getlist('course_num')
        ke = []
        flag = 0
        for temp in couids:
            print(temp)
            #一个一个删除数据
            sql = "delete from t_course_info where course_num = '"+str(temp)+"'"
            result1 = DelDataByIdOne(sql)
            if result1 == '删除成功':
                continue
            else:
                flag = 1
        if flag == 1:
            result = '删除失败'
        else:
            result = '删除成功'
        return redirect(url_for('courseinfo_api.kechenglist', result=result))

#修改开设课程页面
@courseinfo_api.route('/updateCourcePage', methods=['GET'])
def updateCourcePage():
    #将数据查询出来，传递给修改界面
    course_num = request.args.get('course_num')
    course_name = request.args.get('course_name')
    total_hours = request.args.get('total_hours')
    credit = request.args.get('credit')
    course_type = request.args.get('course_type')
    print(course_num)
    print(course_name)
    print(total_hours)
    print(credit)
    print(course_type)
    return render_template("updateCourcePage_cap.html", course_num=course_num, course_name=course_name, total_hours=total_hours, credit=credit, course_type=course_type)


